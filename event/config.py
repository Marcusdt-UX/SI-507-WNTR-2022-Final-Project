class Config:
    SECRET_KEY = 'kdhjgvfcmvyugdiqygiqebudb'


class DevConfig(Config):
    SERVER_NAME = 'localhost'


config = {
    'dev': DevConfig,
    'prod': Config
}
