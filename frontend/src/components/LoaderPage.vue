<template>
    <transition name="modal">
        <div class="modal-mask">
            <div class="modal-wrapper">
                <div id="spinner">

                </div>
                <div id="loading">
                    <p>Loading...</p>
                </div>
            </div>
        </div>
    </transition>
</template>

<script>


export default {
    name: 'LoaderPage',
    props: {
        isLoading: Boolean,
    },
    setup(){

    }
}
</script>

<style scoped>
.modal-mask {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.9);
    transition: opacity 0.3s ease;
    z-index: 1;
}

.modal-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

#spinner {
  border-radius:50%;
  width: 70px;
  height: 70px;
  background:conic-gradient(rgba(255, 255, 255) 5%, var(--color-nav));
  -webkit-mask:radial-gradient(farthest-side,#0000 calc(100% - 15px),#000 0);
  animation:s3 1s infinite linear;
}
@keyframes s3 {to{transform: rotate(1turn)}}

#loading {
    font-size: xx-large;
    font-weight: bolder;
    color: var(--color-nav)
}

</style>