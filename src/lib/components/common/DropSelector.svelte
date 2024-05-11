<script>
    import { onMount } from 'svelte';

    let selected = "Recent";
    let menuIsOpen = false;
  
    function handleOptionClick(event) {
      selected = event.target.innerText;
      toggleMenu();
    }

    function toggleMenu() {
        menuIsOpen = !menuIsOpen;
    }
    

    function handleOutsideClick(event) {
        const dropdown = document.querySelector(".dropdown");

        if (!dropdown.contains(event.target)) {
        menuIsOpen = false;
        }
    }

    // Добавляем обработчик событий для клика вне элемента
    onMount(() => {
        window.addEventListener("click", handleOutsideClick);
        return () => {
        window.removeEventListener("click", handleOutsideClick);
        };
    });


  </script>
  
  <style>
    .dropdown {
        width: 200px;
        position: relative;
        top: 0;

        user-select: none;
    }
    .select {
        background: #282828;
        color: #fff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px rgba(70, 70, 70, 0.735) solid;
        border-radius: 9999px;
        padding: 10px 18px;
        cursor: pointer;
        transition: 0.3s;

        font-size: 14px;
        line-height: 24px;
    }
    .select-clicked {
        border: 1px rgba(193, 193, 193, 0.735) solid;
        /* box-shadow: 0 0 0.8em #26489a; */
    }
    .select:hover {
        background: #363636;
    }
    .select > span{
        background-color: rgba(255, 255, 255, 0);
    }
    .caret {
        width: 0;
        height: 0;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid #fff;
        transition: 0.3s;
    }
    .caret-rotate {
        transform: rotate(180deg);
    }
    .menu {
        list-style: none;
        padding: 6px;
        background: #282828;
        border: 1px solid rgb(80, 80, 80, 0.735);
        border-radius: 24px;
        color: #9fa5b5;
        position: absolute;
        top: 4em;
        left: 50%;
        width: 100%;
        transform: translateX(-50%);
        opacity: 0;
        display: none;
        transition: 0.2s;
        z-index: 1;
    }
    .menu li {
        padding: 10px 24px;
        margin: 4px 0;
        border-radius: 20px;
        cursor: pointer;

        font-size: 14px;
        line-height: 24px;

        color: #c9c9c9;
    }
    .menu li:hover {
        background: #33333398;
    }
    .selected {
        background: #363636 !important;
        color: #fff !important;
        position: relative;
    }
    .selected::after{
        position: absolute;
        top: calc(50% - 8px);

        width: 16px;
        height: 16px;

        right: 24px;

        content: "";

        background-image: url("https://img.icons8.com/?size=512&id=98955&format=png");
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;

        filter: invert(100%);
    }
    .menu.menu-open {
        display: block;
        opacity: 1;
        z-index: 5;
    }
  </style>
  
  <div class="dropdown">
    <div class="select" class:select-clicked={menuIsOpen} on:click={toggleMenu}>
      <span>{selected}</span>
      <div class="caret" class:caret-rotate={menuIsOpen}></div>
    </div>
    <ul class="menu" class:menu-open={menuIsOpen}>
      <li on:click={handleOptionClick} class:selected={selected === "Recent"}>Recent</li>
      <li on:click={handleOptionClick} class:selected={selected === "Older"}>Older</li>
      <li on:click={handleOptionClick} class:selected={selected === "A-Z"}>A-Z</li>
      <li on:click={handleOptionClick} class:selected={selected === "Z-A"}>Z-A</li>
      <li on:click={handleOptionClick} class:selected={selected === "Popular"}>Popular</li>
    </ul>
  </div>
  