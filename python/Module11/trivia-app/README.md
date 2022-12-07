
== Local dev

``` bash
# install python requirements
pip3 install -r back-end-python/tests/requirements.txt

# run the build locally - unit tests and code coverage reports
./local_build.sh

# view the html coverage report
open htmlcov/index.html
```

== Deploy the Backend

``` bash
# build the application
sam build

# deploy
sam deploy --guided
```

When the deployment completes note the `TriviaWebSocketApi` output.  It will look something like this `wss://xxxxxxxxxx.execute-api.ap-southeast-2.amazonaws.com/Prod`.

== Launch the front end

Note: we need nodejs installed to build and run the front end. You might want to use something like [nvm](https://github.com/nvm-sh/nvm) to install nodejs.


Update the `trivia-app/front-end-react/src/config.js` file with the Websocket endpoint that you copied previously.

``` bash
cd front-end-react/
npm install
npm run start
```

Hosting the front end is easy! You can `npm run build` and copy the contents of `build/...` your hosting location, i.e. an s3 bucket.

