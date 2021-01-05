docker run \
    --name=wiktionary-download \
    -v $1:"/word_list_directory_mount" \
    -v $2:"/target_directory_mount" \
    -e LANGUAGE=$3 \
    alaverydev/audio-language-wiktionary-download