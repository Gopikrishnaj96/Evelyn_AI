# index.html_working
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Jarvis</title>
    <link rel="shortcut icon" href="assets/img/icon.ico" type="image/x-icon" />
    <!-- Bootsrap -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
    <!-- Bootsrap icons-->
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
    />

    <!-- Particle js -->
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"
      type="text/javascript"
    ></script>

    <!--Texllate-->
    <link rel="stylesheet" href="assets/vendore/texllate/animate.css" />
    <link rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div class="container">
      <section id="Oval" class="mb-4">
        <!--mb-4 (margin bottom-4)is a bootstrap utility class-->
      </section>
      <section id="SiriWave" class="mb-4" hidden>
        <div class="container">
          <div class="row">
            <div class="col-md-12">
              <div
                class="d-flex justify-content-center align-items-center"
                style="height: 100vh"
              >
                <div class="">
                  <p
                    class="text-start text-light mb-4 siri-message"
                    style="font-size: 28px"
                  >
                    Hello, I am Eve
                  </p>
                  <div id="siri-container"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
    <div class="row">
      <div class="col-md-1"></div>
      <div class="col-md-30">
        <div
          class="d-flex justify-content-center align-items-center"
          style="height: 70vh"
        >
          <canvas
            id="canvasOne"
            width="700"
            height="420"
            style="position: absolute"
          >
          </canvas>
          <div id="JarvisHood">
            <div class="square">
              <span class="circle"></span>
              <span class="circle"></span>
              <span class="circle"></span>
            </div>
          </div>
        </div>
        <h5 class="text-light text text-center" style="height: 13vh" ;>
          Feel free to ask me anything!
        </h5>
        <div class="col-md-12">
          <div class="text-center">
            <div id="TextInput" class="d-flex">
              <input
                type="text"
                class="input-field"
                name="chatbox"
                id="chatbox"
                placeholder="type here"
              />
              <button id="SendBtn" class="glow-on-hover" hidden>
                <i class="bi bi-send"></i>
              </button>
              <button id="MicBtn" class="glow-on-hover">
                <i class="bi bi-mic-fill"></i>
              </button>
              <button id="ChatBtn" class="glow-on-hover">
                <i class="bi bi-chat-text-fill"></i>
              </button>
              <button id="SettingsBtn" class="glow-on-hover">
                <i class="bi bi-gear-fill"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-1"></div>
    </div>

    <!--Jquery  -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <!-- Bootsrap -->
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
      crossorigin="anonymous"
    ></script>

    <!-- Particle js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js"></script>
    <script src="script.js"></script>

    <!--Siri wave-->
    <script src="https://unpkg.com/siriwave/dist/siriwave.umd.min.js"></script>

    <!--Texllate js-->
    <script src="assets/vendore/texllate/jquery.lettering.js"></script>
    <script src="assets/vendore/texllate/jquery.fittext.js"></script>
    <script src="http://jschr.github.io/textillate/jquery.textillate.js"></script>
    `

    <script src="main.js"></script>
    <script src="controller.js"></script>
    <script src="/eel.js"></script>
  </body>
</html>

