new Vue({
    el: '#all',
    data: {
        selectedStyle: 'lightMode',
        image: 'assets/sun.png',
        iconClass: 'modeIcon sun',
        isDarkMode: false,
    },
    watch:{
        isDarkMode(newVal){
            this.selectedStyle = newVal ? 'darkMode' : 'lightMode';
            this.image = newVal ? 'assets/moon.png' : 'assets/sun.png';
            this.iconClass = newVal ? 'modeIcon moon' : 'modeIcon sun';
        }
    }
});