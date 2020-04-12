amixer set PCM -- 100%
echo $1 | festival --tts
amixer set PCM -- $2%
echo "Done"