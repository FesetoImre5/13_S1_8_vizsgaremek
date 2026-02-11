import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import hu from './locales/hu.json'

const i18n = createI18n({
    legacy: false, // you must set `false`, to use Composition API
    locale: 'en', // set locale
    fallbackLocale: 'en', // set fallback locale
    messages: {
        en,
        hu
    }
})

export default i18n
