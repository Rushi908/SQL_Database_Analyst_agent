import os
import re
import yaml


ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")


def resolve_env_variables(value):
    """
    Recursively replace ${ENV_VAR} with environment variable values.
    """

    if isinstance(value, dict):
        return {
            key: resolve_env_variables(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            resolve_env_variables(item)
            for item in value
        ]

    if isinstance(value, str):
        def replace(match):
            env_name = match.group(1)

            env_value = os.getenv(env_name)

            if env_value is None:
                raise RuntimeError(
                    f"Environment variable '{env_name}' is not set."
                )

            return env_value

        return ENV_PATTERN.sub(replace, value)

    return value


def load_config(path="config/agent.yaml"):

    with open(path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    config = resolve_env_variables(config)

    return config