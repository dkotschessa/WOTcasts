echo Saving podcasts to fixture
echo before...
ls -l loadpods.json
 ./manage.py dumpdata podcasts.podcast > loadpods.json
echo after...
ls -l loadpods.json
 
