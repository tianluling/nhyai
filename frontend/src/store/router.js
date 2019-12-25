
import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter);

//实现懒加载
const sindex=resolve=>require(['../views/sindex'],resolve);
const imageRecognition=resolve=>require(['../views/image_recognition'],resolve);
const idCard=resolve=>require(['../views/OCRRecognition/id_card'],resolve);
const drivingLicence=resolve=>require(['../views/OCRRecognition/driving_licence'],resolve);
const runningLicence=resolve=>require(['../views/OCRRecognition/running_licence'],resolve);
const commonUse=resolve=>require(['../views/OCRRecognition/common_use'],resolve);
const businessLicence=resolve=>require(['../views/OCRRecognition/business_licence'],resolve);
const bankCard=resolve=>require(['../views/OCRRecognition/bank_card'],resolve);
const handwriten=resolve=>require(['../views/OCRRecognition/handwriten'],resolve);
const carNumber=resolve=>require(['../views/OCRRecognition/car_number'],resolve);
const visitingCard=resolve=>require(['../views/OCRRecognition/visiting_card'],resolve);
const yellow=resolve=>require(['../views/yellow'],resolve);
const force=resolve=>require(['../views/force'],resolve);
const wordRecognition=resolve=>require(['../views/wordRecognition'],resolve);
const voiceRecognition=resolve=>require(['../views/voiceRecognition'],resolve);
const videoRecognition=resolve=>require(['../views/videoRecognition'],resolve);
const writeRecognition=resolve=>require(['../views/writeRecognition'],resolve);
const record=resolve=>require(['../views/record'],resolve);

Vue.config.productionTip = false

//路由配置
const router = new VueRouter({
    mode: 'history',
    base: process.env.NODE_ENV === 'production'? '': '',
    linkActiveClass:'active',

    routes: [
        {path:'/sindex',meta:{title:'人工智能-南海云AI平台-AI智能审核',keepAlive:true},component:sindex},
        {path:'/imageRecognition',meta:{title:'ORC识别-南海云AI平台'},component:imageRecognition,
            children:[
                {path:'idCard',meta:{title:'OCR识别-南海云AI平台'},component:idCard},
                {path:'drivingLicence',meta:{title:'OCR识别-南海云AI平台'},component:drivingLicence},
                {path:'runningLicence',meta:{title:'OCR识别-南海云AI平台'},component:runningLicence},
                {path:'commonUse',meta:{title:'OCR识别-南海云AI平台'},component:commonUse},
                {path:'businessLicence',meta:{title:'OCR识别-南海云AI平台'},component:businessLicence},//营业执照
                {path:'bankCard',meta:{title:'OCR识别-南海云AI平台'},component:bankCard},    //银行卡
                {path:'handwriten',meta:{title:'OCR识别-南海云AI平台'},component:handwriten},//手写体
                {path:'carNumber',meta:{title:'OCR识别-南海云AI平台'},component:carNumber},  //车牌
                {path:'visitingCard',meta:{title:'OCR识别-南海云AI平台'},component:visitingCard},  //名片
                {path:'/',redirect:'idCard'},
        ]},
        {path:'/yellow',meta:{title:'色情识别-南海云AI平台'},component:yellow},  //名片
        {path:'/force',meta:{title:'暴恐识别-南海云AI平台'},component:force},  //名片
        {path:'/wordRecognition',meta:{title:'文本检测-南海云AI平台'},component:wordRecognition,
            children:[
                {path:'idCard',meta:{title:'文本检测-南海云AI平台'},component:idCard},
                {path:'drivingLicence',meta:{title:'文本检测-南海云AI平台'},component:drivingLicence},
                {path:'runningLicence',meta:{title:'文本检测-南海云AI平台'},component:runningLicence},
                {path:'commonUse',meta:{title:'文本检测-南海云AI平台'},component:commonUse},
                {path:'businessLicence',meta:{title:'文本检测-南海云AI平台'},component:businessLicence},//营业执照
                {path:'bankCard',meta:{title:'文本检测-南海云AI平台'},component:bankCard},    //银行卡
                {path:'handwriten',meta:{title:'文本检测-南海云AI平台'},component:handwriten},//手写体
                {path:'carNumber',meta:{title:'文本检测-南海云AI平台'},component:carNumber},  //车牌
                {path:'visitingCard',meta:{title:'文本检测-南海云AI平台'},component:visitingCard},  //名片
                {path:'/',redirect:'idCard'},
            ]},
        {path:'/voiceRecognition',meta:{title:'语音识别-南海云AI平台'},component:voiceRecognition},  //语音识别
        {path:'/writeRecognition',meta:{title:'文本检测-南海云AI平台'},component:writeRecognition},  //语音识别
        {path:'/videoRecognition',meta:{title:'视频识别-南海云AI平台',keepAlive:true},component:videoRecognition},  //视频识别


        {path:'/',redirect:'/sindex'}
    ],

});

router.beforeEach((to, from, next) => {
    next();
    document.title=to.meta.title;
});

export default router;
