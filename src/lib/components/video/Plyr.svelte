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
        <div class="plyr__video-embed">
            <iframe
              src="https://www.youtube.com/watch?v=wi08uYZBhRs&iv_load_policy=3&modestbranding=1&playsinline=1&showinfo=0&rel=0&enablejsapi=1"
              allowfullscreen allowtransparency allow="autoplay">
            </iframe>
          </div>
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