<script>
    import { Plyr } from "svelte-plyr";
    import { SUPPORTED_FILE_TYPE, SUPPORTED_FILE_EXTENSIONS, WEBUI_BASE_URL } from '$lib/constants';
    export let videoId;
  
    function logEvent(event) {
      console.log(event)
    }
  
    let player
  </script>
  
  <div class="youtube-plyr">
    <!-- <button on:click={() => player.play()}>PLAY</button>
    <button on:click={() => player.pause()}>PAUSE</button> -->
    <Plyr on:timeupdate={logEvent} bind:player={player}>
        <video
    crossorigin
    playsinline
    poster="https://m.media-amazon.com/images/I/81QBt4prTuL._AC_UF1000,1000_QL80_.jpg"
    src="/Users/daniil/Desktop/Работа/NewNeuroGPT/open-webui/static/example_video.mp4"
  >
    <source
      src="/Users/daniil/Desktop/Работа/NewNeuroGPT/open-webui/static/example_video.mp4"
      type="video/mp4"
    >
  </video>
    </Plyr>
  </div>
  
  <style>
    :root {
  --plyr-color-main: #B4B4B4;
}
  .youtube-plyr {
    max-width: 100%;
    border-radius: 20px;
    overflow: hidden;
  }
  </style>