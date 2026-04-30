from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    STEM_AGENT_MODEL: str
    EVALUATOR_MODEL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()