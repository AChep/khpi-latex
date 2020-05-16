import * as firebase from 'firebase';

const config = {
    apiKey: "AIzaSyA-IDrxtlqu6026Cf0dNCYoZN0HT-qetCw",
    authDomain: "scheduleachep.firebaseapp.com",
    databaseURL: "https://scheduleachep.firebaseio.com",
    projectId: "scheduleachep",
    storageBucket: "scheduleachep.appspot.com",
    messagingSenderId: "188058837416",
    appId: "1:188058837416:web:4c2e68bd058bb948d57d9d"
};
firebase.initializeApp(config);

export default firebase;
