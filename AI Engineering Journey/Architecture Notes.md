Why does try/except stay inside ai_service?

Because the service that knows how to communicate with OpenAI
is responsible for handling OpenAI errors.

Principle:
Handle the error as close as possible to where it happens.

## Error handling

Handle errors as close as possible to where they happen.

Example:
OpenAI errors are handled inside ai_service.py because that module is responsible for communicating with the API.

## Personality

A helpful companion who knows how to help without overwhelming the user.