<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

  
    let isDesktop = false;
  
    onMount(async () => {
      // Проверка размера экрана для показа навигации на десктопе
      isDesktop = window.innerWidth >= 768;
      window.addEventListener('resize', () => {
        isDesktop = window.innerWidth >= 768;
      });
    });
  
    function handleNavigation(path) {
      goto(path);
    }

  </script>
  
  <style>
    .header {
      position: absolute;
      width: 100%;
      z-index: 30;
    }
    .max-w-6xl {
      max-width: 72rem;
    }
    .flex {
      display: flex;
    }
    .items-center {
      align-items: center;
    }
    .justify-between {
      justify-content: space-between;
    }
    .h-20 {
      height: 5rem;
    }
    .shrink-0 {
      flex-shrink: 0;
    }
    .mr-4 {
      margin-right: 1rem;
    }
    .hidden {
      display: none;
    }
    .md\\:flex {
      display: flex;
    }
    .md\\:grow {
      flex-grow: 1;
    }
    .text-white {
      color: white;
    }
    .hover\\:text-gray-200:hover {
      color: #e5e7eb;
    }
    .px-4 {
      padding-left: 1rem;
      padding-right: 1rem;
    }
    .py-3 {
      padding-top: 0.75rem;
      padding-bottom: 0.75rem;
    }
    .transition {
      transition: all 0.15s ease-in-out;
    }
    .btn-sm {
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      font-size: 0.875rem;
    }
    .bg-white {
      background-color: white;
    }
    .hover\\:bg-purple-500:hover {
      background-color: #9f7aea;
    }
    .ml-3 {
      margin-left: 0.75rem;
    }

    .button_start{
        background-color: rgba(255, 255, 255, 0);
        border: 1px solid white;
        color: white;

        border-radius: 20px;

        transition: all .2s ease-in-out;
    }

    .button_start:hover{
        background-color: white;
        color: black;
    }
  </style>
  
  <header class="header">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-20">
        <!-- Site branding -->
        <div class="shrink-0 mr-4">
          <!-- Logo -->
          <a href="/" class="block" aria-label="Cruip" style="width: 40px; height: 40px; filter: invert(100%);">
            <svg width="100%" height="100%" viewBox="0 0 500 500" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="347.666" y="139" width="44.3349" height="221.675" fill="black"/>
              <path fill-rule="evenodd" clip-rule="evenodd" d="M202.643 360.287C263.75 360.287 313.287 310.75 313.287 249.643C313.287 188.537 263.75 139 202.643 139C141.537 139 92 188.537 92 249.643C92 310.75 141.537 360.287 202.643 360.287ZM202.645 316.029C239.309 316.029 269.031 286.307 269.031 249.643C269.031 212.979 239.309 183.257 202.645 183.257C165.981 183.257 136.259 212.979 136.259 249.643C136.259 286.307 165.981 316.029 202.645 316.029Z" fill="black"/>
            </svg>
          </a>
        </div>
  
        <!-- Desktop navigation -->
        {#if isDesktop}
          <nav class="md:flex md:grow">
            <!-- Desktop sign in links -->
            <ul class="flex grow justify-end flex-wrap items-center">
              <li>
                <a
                  href="/"
                  class="button_start font-medium text-white hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out"
                  on:click|preventDefault={() => handleNavigation('/auth')}
                >
                  Start now
                </a>
              </li>
            </ul>
          </nav>
        {/if}
      </div>
    </div>
  </header>
  