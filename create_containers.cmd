docker create ^
    -v %cd%/text_source.txt:/usr/src/app/text_source.txt ^
    -v %cd%/settings.py:/usr/src/app/settings.py ^
    --name screaming-bot-text-reader ^
    --entrypoint python ^
    alphadock/screaming-bot:latest ^
    get_tumblr_posts.py

docker create ^
    -v %cd%/text_source.txt:/usr/src/app/text_source.txt ^
    -v %cd%/settings.py:/usr/src/app/settings.py ^
    --entrypoint python ^
    --name screaming-bot-post-generator ^
    alphadock/screaming-bot:latest ^
    generate_post.py