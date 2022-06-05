/*
peshkin_mv, 2022
*/

class MPlayer {
    constructor(options={}){
        this.currentSrc = '';
        this.audio = null;
        this.slider = null;
        this.slidebar = null;
        this.playing = false;
        this.btn = null;
        this.nowPlaying = '';
        this.playSpeedMenu = null;
        this.playbackRate = 1;

        for(let opt in options){
            if(this[opt] !== undefined){
                this[opt] = options[opt];
            }
        }

        if(this.slider && this.slidebar){
            slidebar.addEventListener('click', (e) => {
                if(!this.audio.src){
                    return;
                }

                const rect = slidebar.getBoundingClientRect();
                const x = rect.left;
                const percent = ((e.clientX - x)*100)/rect.width;
                this.slider.style.width = `${percent}%`;
                if(this.audio){
                    this.setCurrentPos(percent);
                }
            });
        }

        const _audio = this.audio;

        _audio.ontimeupdate = (e) => {
            this.slider.style.width = `${(_audio.currentTime*100)/_audio.duration}%`;
        }

        _audio.onended = (e) => {
            this.playing = false;
            this.toggleBtn(this.btn);
            this.toggleSecondary();
        }

        if(this.playSpeedMenu){
            this.playSpeedMenu.querySelectorAll('li').forEach((e, o, a) => {
                e.addEventListener('click', (ev) => {
                    ev.preventDefault();
                    this.setPlaybackRate(parseFloat(parseFloat(e.textContent)));
                });
            });    
        }

        if(this.btn){
            this.btn.addEventListener('click', (e) => {
                if(!this.audio.src){
                    return;
                }

                if(this.isPlaying()){
                    this.pause();
                } else {
                    this.play();
                }

                this.toggleBtn(this.btn);
                this.toggleSecondary();
            });
        }
    }

    setPlaybackRate(rate){
        this.playbackRate = rate;
        this.audio.playbackRate = this.playbackRate;
    }

    changeTrack(src){
        this.audio.pause();
        this.audio.currentTime = 0.0;
        this.audio.src = src;
        this.currentSrc = src;
    }

    play(){
        this.setPlaybackRate(this.playbackRate);
        this.audio.play();
        this.playing = true;
    }

    pause(){
        this.audio.pause();
        this.playing = false;
    }

    isPlaying(){
        return this.playing;
    }

    toggleBtn(btn){
        if(!btn){
            return;
        }

        const i = btn.querySelector('i');
        if(i.classList.contains('icon-stop')){
            i.classList.replace('icon-stop', 'icon-arrow-right');  
        } else {
            i.classList.replace('icon-arrow-right', 'icon-stop');
        }
    }

    toggleSecondary(){
        this.toggleBtn(this.btnSecondary);       
    }

    setCurrentPos(percent){
        this.audio.currentTime = (this.audio.duration/100)*percent;
    }
}