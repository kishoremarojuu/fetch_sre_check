import argparse
import asyncio
import yaml
from utils import check_endpoint, extract_domain, log_availability

AVAILABILITY = {}

async def run_checks(endpoints):
    tasks = [check_endpoint(ep, AVAILABILITY) for ep in endpoints]
    await asyncio.gather(*tasks)

async def main(config_path):
    with open(config_path) as f:
        endpoints = yaml.safe_load(f)

    while True:
        await run_checks(endpoints)
        log_availability(AVAILABILITY)
        await asyncio.sleep(15)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Path to YAML config file')
    args = parser.parse_args()

    try:
        asyncio.run(main(args.config))
    except KeyboardInterrupt:
        print("\nStopped by user.")
