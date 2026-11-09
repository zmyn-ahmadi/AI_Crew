import json

from openai import OpenAI
from pydantic import validate_call

from llm.spinner import Spinner
from tools.schemas import tool_schema


class LLM:
    def __init__(
        self,
        base_url="http://localhost:8080/v1",
        api_key="none",
        model="local",
        stream=True,
        tools=None,
        instructions="",
    ):
        self.base_url = base_url
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.stream = stream
        self.instructions = instructions

        self.history = []

        tools = tools or []
        self.tools = [tool_schema(fn) for fn in tools]  # list of tools json
        self.tool_fns = {
            fn.__name__: validate_call(fn) for fn in tools
        }  # {"function name": fn}

    def run(self, prompt, schema=None):
        self.history = [{"role": "user", "content": prompt}]
        text = self._run_turn(schema)
        return schema.model_validate_json(text) if schema else text

    def _run_turn(self, schema=None):
        """Ask the model, run any tools it calls, repeat until it answers in text."""
        seen = set()

        while True:
            # llama-server can't combine tool and json_schema grammars in one request,
            # so with tools the schema is applied in a final tool-less turn.
            response = self._reply(None if self.tools else schema)
            calls = [item for item in response.output if item.type == "function_call"]

            if not calls:
                if schema and self.tools:
                    response = self._reply(schema, use_tools=False)
                return response.output_text or ""

            for call in calls:
                # Local models repeat calls, and each full copy eats the context.
                key = (call.name, call.arguments)
                if key in seen:
                    output = (
                        '{"note": "Same call already returned above. Use that result."}'
                    )
                else:
                    output = self._run_tool(call)
                seen.add(key)

                self.history.append(
                    {
                        "type": "function_call",
                        "call_id": call.call_id,
                        "name": call.name,
                        "arguments": call.arguments,
                    }
                )
                self.history.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": output,
                    }
                )

    def _run_tool(self, call):
        try:
            args = json.loads(call.arguments or "{}")
            return json.dumps(self.tool_fns[call.name](**args))
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _reply(self, schema=None, use_tools=True):
        kwargs = {}
        if schema:
            kwargs["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": schema.__name__,
                    "schema": schema.model_json_schema(),
                    "strict": True,
                }
            }
            # llama-server ignores text.format on /v1/responses; its own json_schema field is enforced.
            kwargs["extra_body"] = {"json_schema": schema.model_json_schema()}

        with Spinner():
            response = self.client.responses.create(
                model=self.model,
                instructions=self.instructions,
                input=self.history,
                tools=self.tools if use_tools else [],
                stream=self.stream,
                **kwargs,
            )
            if not self.stream:
                return response

            for event in response:
                if event.type == "response.completed":
                    return event.response

        raise RuntimeError("Stream ended without a completed response")
