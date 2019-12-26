<template id="audioSample">
	<div class="voice_player_outer clearfix">
		<img src="../assets/image/voice_mark.png" class="fl icon_music" id="music_icon">
		<div class="audio_wrapper_outer">

			<div class="audio-wrapper">
				<audio id="audio">
					<source :src="recordSrc" type="audio/wav">
				</audio>
				<div class="audio-left">
					<img id="audioPlayer" src="../assets/image/audio/play.png">
				</div>
				<div class="audio-right">
					<div class="progress-bar-bg" id="progressBarBg">
						<span id="progressDot"></span>
						<div class="progress-bar" id="progressBar"></div>
					</div>
					<div class="audio-time">
						<span class="audio-length-current" id="audioCurTime">00:00</span>
						<span class="audio-length-total"></span>
					</div>
					<p style="max-width: 536px;">{{audioName}}</p>
				</div>
			</div>
		</div>

	</div>
</template>

<script >
	export default {
        props:['recordSrc'],
	    data(){
	        return{
                imageIsBig:false,
//                recordSrc:"",
                resultType:[],
                audioName:'',
                isNone:true,
                isUploading:false,
                isSex:false,
                isForce:false,
                isSong:false,
                isPolitics:false
			}
		},
        mounted(){
            this.initAudioEvent();
//            this.recordSrc = URL.createObjectURL(file);
			console.log(this.recordSrc)
            const audio = document.getElementById('audio');
            audio.play()
        },
        watch:{
            stopAudio:(newVal)=>{
                if(newVal){
                    const audio = document.getElementById('audio');
                    const audioPlayer = document.getElementById('audioPlayer');
                    const musicIcon = document.getElementById('music_icon');
                    console.log(newVal);
                    audio.pause();
                    audioPlayer.src =require( '../assets/image/audio/play.png');
                    musicIcon.src =require( '../assets/image/voice_mark.png');
                }
            }
        },
        methods:{
            initAudioEvent(){
                console.log('执行到这里了')
                var audio = document.getElementsByTagName('audio')[0];
                var audioPlayer = document.getElementById('audioPlayer');
                var musicIcon = document.getElementById('music_icon');
                // 监听音频播放时间并更新进度条
                audio.addEventListener('timeupdate', ()=>{
                    this.updateProgress(audio);
                }, false);

                // 监听播放完成事件
                audio.addEventListener('ended', ()=> {
                    this.audioEnded();
                }, false);

                // 点击播放/暂停图片时，控制音乐的播放与暂停
                audioPlayer.addEventListener('click', ()=> {
                    // 改变播放/暂停图片
                    if (audio.paused) {
                        console.log('播放');
                        // 开始播放当前点击的音频
                        this.timeout1 = setTimeout(()=>{
                            audio.play()
                        },300)
                        audioPlayer.src =require('../assets/image/audio/pause.png') ;
                        musicIcon.src = require('../assets/image/audio/icon-music.gif');
                    } else {
                        console.log('暂停');
                        audio.pause();
                        audioPlayer.src =require( '../assets/image/audio/play.png');
                        musicIcon.src = require('../assets/image/voice_mark.png');
                    }
                }, false);

                // 点击进度条跳到指定点播放
                // PS：此处不要用click，否则下面的拖动进度点事件有可能在此处触发，此时e.offsetX的值非常小，会导致进度条弹回开始处（简直不能忍！！）
                var progressBarBg = document.getElementById('progressBarBg');
                progressBarBg.addEventListener('mousedown', (event)=> {
                    // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
                    if (!audio.paused || audio.currentTime != 0) {
                        var pgsWidth = parseFloat(window.getComputedStyle(progressBarBg, null).width.replace('px', ''));
                        var rate = event.offsetX / pgsWidth;
                        audio.currentTime = audio.duration * rate;
                        this.updateProgress(audio);
                    }
                }, false);

                // 拖动进度点调节进度
                this.dragProgressDotEvent(audio);
            },

            /**
             * 鼠标拖动进度点时可以调节进度
             * @param {*} audio
             */
            dragProgressDotEvent(audio) {
                var dot = document.getElementById('progressDot');

                var position = {
                    oriOffestLeft: 0, // 移动开始时进度条的点距离进度条的偏移值
                    oriX: 0, // 移动开始时的x坐标
                    maxLeft: 0, // 向左最大可拖动距离
                    maxRight: 0 // 向右最大可拖动距离
                };
                var flag = false; // 标记是否拖动开始

                // 鼠标按下时
                dot.addEventListener('mousedown', down, false);
                dot.addEventListener('touchstart', down, false);

                // 开始拖动
                document.addEventListener('mousemove', move, false);
                document.addEventListener('touchmove', move, false);

                // 拖动结束
                document.addEventListener('mouseup', end, false);
                document.addEventListener('touchend', end, false);

                function down(event) {
                    if (!audio.paused || audio.currentTime != 0) { // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
                        flag = true;

                        position.oriOffestLeft = dot.offsetLeft;
                        position.oriX = event.touches ? event.touches[0].clientX : event.clientX; // 要同时适配mousedown和touchstart事件
                        position.maxLeft = position.oriOffestLeft; // 向左最大可拖动距离
                        position.maxRight = document.getElementById('progressBarBg').offsetWidth - position.oriOffestLeft; // 向右最大可拖动距离

                        // 禁止默认事件（避免鼠标拖拽进度点的时候选中文字）
                        if (event && event.preventDefault) {
                            event.preventDefault();
                        } else {
                            event.returnValue = false;
                        }

                        // 禁止事件冒泡
                        if (event && event.stopPropagation) {
                            event.stopPropagation();
                        } else {
                            window.event.cancelBubble = true;
                        }
                    }
                }

                function move(event) {
                    if (flag) {
                        var clientX = event.touches ? event.touches[0].clientX : event.clientX; // 要同时适配mousemove和touchmove事件
                        var length = clientX - position.oriX;
                        if (length > position.maxRight) {
                            length = position.maxRight;
                        } else if (length < -position.maxLeft) {
                            length = -position.maxLeft;
                        }
                        var progressBarBg = document.getElementById('progressBarBg');
                        var pgsWidth = parseFloat(window.getComputedStyle(progressBarBg, null).width.replace('px', ''));
                        var rate = (position.oriOffestLeft + length) / pgsWidth;
                        audio.currentTime = audio.duration * rate;
                        this.updateProgress(audio);
                    }
                }

                function end() {
                    flag = false;
                }
            },

            /**
             * 停止播放
             * */
            pauseAudio(){
                var audio = document.getElementsByTagName('audio')[0];
                var audioPlayer = document.getElementById('audioPlayer');
                var musicIcon = document.getElementById('music_icon');
                audio.stop();
                audioPlayer.src =require( '../assets/image/audio/play.png');
                musicIcon.src =require( '../assets/image/voice_mark.png');
            },

            /**
             * 更新进度条与当前播放时间
             * @param {object} audio - audio对象
             */
            updateProgress(audio) {
                var value = audio.currentTime / audio.duration;
                document.getElementById('progressBar').style.width = value * 100 + '%';
                document.getElementById('progressDot').style.left = value * 100 + '%';
                document.getElementById('audioCurTime').innerText = this.transTime(audio.currentTime);
                document.getElementsByClassName('audio-length-total')[0].innerText = this.transTime(audio.duration);
            },

            /**
             * 播放完成时把进度调回开始的位置
             */
            audioEnded() {
                document.getElementById('progressBar').style.width = 0;
                document.getElementById('progressDot').style.left = 0;
                document.getElementById('audioCurTime').innerText = this.transTime(0);
                document.getElementById('audioPlayer').src =require( '../assets/image/audio/play.png');
                document.getElementById('music_icon').src =require( '../assets/image/voice_mark.png');
            },

            /**
             * 音频播放时间换算
             * @param {number} value - 音频当前播放时间，单位秒
             */
            transTime(value) {
                var time = "";
                var h = parseInt(value / 3600);
                value %= 3600;
                var m = parseInt(value / 60);
                var s = parseInt(value % 60);
                if (h > 0) {
                    time = this.formatTime(h + ":" + m + ":" + s);
                } else {
                    time = this.formatTime(m + ":" + s);
                }

                return time;
            },

            /**
             * 格式化时间显示，补零对齐
             * eg：2:4  -->  02:04
             * @param {string} value - 形如 h:m:s 的字符串
             */
            formatTime(value) {
                var time = "";
                var s = value.split(':');
                var i = 0;
                for (; i < s.length - 1; i++) {
                    time += s[i].length == 1 ? ("0" + s[i]) : s[i];
                    time += ":";
                }
                time += s[i].length == 1 ? ("0" + s[i]) : s[i];

                return time;
            },
        }
	}

</script>

<style >
	@import "../assets/css/audio.css";
	.voice_player_outer{height: 125px;width: 94%;margin: 10px auto;border-radius: 5px;background-color: white;}
	.audio_wrapper_outer{margin-left: 180px;margin-right: 20%;}
	.icon_music{margin: 25px 0 0 95px;}
	.show_voice_word{margin: 20px ;color: #010101;font-size: 14px;display: flex}
	.show_voice_word span{display: inline-block;text-align: left;}
	.show_voice_word span:nth-of-type(2){margin-left: 20px;flex: 1;}

</style>