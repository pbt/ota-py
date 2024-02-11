# OTA (The Octopus Transit Agency)

_the countdown clock i wanted to see_

this is a subway countdown clock so you can see when you need to run to catch the train. there are others like it, but i like how mine looks :)

maybe 50% working at the moment.

you can see it [here](https://ota.pbt.dev).

## serving suggestions
throw it on a [TV](https://rctv.recurse.com/) or install it as a progressive webapp on your phone or computer!

## getting started
1. get an API key from the [MTA](https://api.mta.info/#/landing)
2. `poetry install`
3. `API_KEY=${YOUR_API_KEY} poetry run hypercorn app:asgi_app`
