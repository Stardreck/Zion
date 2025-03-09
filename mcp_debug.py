from src.star_config import StarConfig
from src.star_engine import StarEngine


def main():
    config = StarConfig("data/star_config.json")
    engine = StarEngine(config)

if __name__ == "__main__":
    main()