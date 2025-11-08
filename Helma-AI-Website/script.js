const firebaseConfig = {
  apiKey: "AIzaSyCpGYArcsTpQw_AWRGrXS9OlpB1k1qdd5A",
  authDomain: "helma-ai-website.firebaseapp.com",
  projectId: "helma-ai-website",
  storageBucket: "helma-ai-website.firebasestorage.app",
  messagingSenderId: "398709747893",
  appId: "1:398709747893:web:785d386f509e2cc4efcefc"
};

const app = firebase.initializeApp(firebaseConfig);
const functions = firebase.functions();

// --- Translations ---
const translations = {
    tr: {
        appName: "Helma AI",
        appSubtitle: "HealthMate",
        navHome: "Ana Sayfa",
        navFeatures: "Özellikler",
        navTeam: "Ekip",
        navContact: "İletişim",
        navCta: "Haberdar Ol",
        heroTitle: 'Sevdikleriniz İçin<span class="block text-blue-500 mt-2">Akıllı Sağlık Asistanı</span>',
        heroSubtitle: '<span class="block text-balance hero-subtext-primary">Helma AI, yapay zekâ destekli mobil refakatçisi ile yaşlı bireylerin daha güvenli, sağlıklı ve bağımsız bir yaşam sürmesine destek olur.</span><span class="block mt-6 text-balance hero-subtext-secondary">Günlük rutinleri hassasiyetle takip eder, ihtiyaç anlarında yakınları bilgilendirir ve <span class="font-semibold text-blue-400">kişiselleştirilmiş önerilerle</span> yaşam kalitesini sürekli iyileştirir.</span>',
        heroCta: "Daha Fazlasını Keşfet",
        featuresTitle: "Kapsamlı Çözümlerimiz",
        featuresSubtitle: "Günlük yaşamı kolaylaştıran, güvenliği artıran ve sosyal bağları güçlendiren yenilikçi özellikler.",
        feature1Title: "Yapay Zekâ Refakatçisi",
        feature1Desc: "Görüntülü görüşmelerde duygu analizi yaparak kullanıcıların hâlini anlayan, sohbet eden akıllı asistan.",
        feature2Title: "Canlı Görüntülü Bağlantı",
        feature2Desc: "Yakınlar ve bakım verenlerle tek dokunuşla HD video aramalarını başlatır, güvenli iletişim sunar.",
        feature3Title: "İlaç & Su Hatırlatıcısı",
        feature3Desc: "Kişiselleştirilmiş saatlerde ilaç ve su uyarıları göndererek sağlıklı rutinlerin devamını destekler.",
        feature4Title: "Egzersiz Önerileri",
        feature4Desc: "Kondisyona uygun günlük hareket ve esneme programlarıyla aktif yaşamı teşvik eder.",
        feature5Title: "Hava & Haber Panosu",
        feature5Desc: "Güncel hava durumu ve haber özetlerini sade bir akışta sunarak bilgilendirir.",
        feature6Title: "Acil Durum ve Sesli Destek",
        feature6Desc: "Acil durum butonu ve sesli yardım çağrısıyla ihtiyaç anında yakınlara anında bildirim gönderir.",
        feature7Title: "Zihin Egzersizleri",
        feature7Desc: "Günlük bulmacalar, hafıza oyunları ve sohbet görevleriyle bilişsel becerileri canlı tutar.",
        feature8Title: "Kişisel Rutin Tanıma",
        feature8Desc: "Alışkanlıkları analiz ederek gün içinde en doğru zamanda öneriler ve hatırlatmalar sunar.",
        feature9Title: "Haftalık Sağlık Raporları",
        feature9Desc: "Yaşam belirtileri ve aktivite verilerini derleyip aile üyeleriyle paylaşılabilir raporlar üretir.",
        feature10Title: "Duygu Analizi ile Destek",
        feature10Desc: "Konuşma ve yüz ifadelerinden ruh hâlini izleyip pozitif motivasyon mesajları gönderir.",
        teamTitle: "Proje Ekibi",
        teamSubtitle: 'Teknolojiyi toplumsal fayda için kullanma vizyonuyla bir araya gelmiş<br class="hidden sm:block">5 bilgisayar mühendisliği öğrencisi.',
        teamMember1Name: "Ulaş UÇRAK",
        teamMember1Role: "Proje Yöneticisi & Yapay Zekâ Geliştiricisi",
        teamMember1Desc: "Model geliştirme sürecini yönetir, proje planını takip eder ve ekibi koordine eder.",
        teamMember2Name: "Arda YILDIZ",
        teamMember2Role: "Mobil Geliştirici (iOS & Android)",
        teamMember2Desc: "Çok platformlu uygulama deneyimini optimize eder, performans ve güvenilirliği sağlar.",
        teamMember3Name: "Barkın SARIKARTAL",
        teamMember3Role: "Araştırma & Entegrasyon Sorumlusu",
        teamMember3Desc: "Yeni teknolojileri araştırır, dış servis entegrasyonlarını planlar ve uygular.",
        teamMember4Name: "Doğukan POYRAZ",
        teamMember4Role: "Backend & Veri Tabanı Geliştiricisi",
        teamMember4Desc: "Sunucu mimarisini, veri işleme akışını ve güvenli veri depolamayı inşa eder.",
        teamMember5Name: "Umut Eray AÇIKGÖZ",
        teamMember5Role: "Yapay Zekâ Geliştiricisi",
        teamMember5Desc: "Geliştirilen modellerin pipeline ve füzyon süreçlerini tasarlar.",
        contactTitle: "Gelişmelerden Haberdar Olun!",
        contactSubtitle: "Helma AI uygulaması yayınlandığında ilk duyan siz olmak için e-posta listemize kaydolun.",
        emailPlaceholder: "E-posta adresiniz",
        subscribeButton: "Kaydol",
        formSubmitting: "Kaydediliyor…",
        formSuccess: "Başarıyla kaydoldunuz! Teşekkür ederiz.",
        formErrorInvalid: "Lütfen geçerli bir e-posta adresi girin.",
        formErrorDuplicate: "Bu e-posta adresi zaten listemizde.",
        formErrorServer: "Sunucu tarafında bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
        formErrorGeneric: "Bir hata oluştu. Lütfen tekrar deneyin.",
        footerSlogan: "Yaşlı bireylerin yaşam kalitesini teknoloji ile artırıyoruz.",
        footerFollow: "Bizi Takip Edin",
        footerRights: "&copy; 2025 Helma AI. Tüm hakları saklıdır.",
    },
    en: {
        appName: "Helma AI",
        appSubtitle: "HealthMate",
        navHome: "Home",
        navFeatures: "Features",
        navTeam: "Team",
        navContact: "Contact",
        navCta: "Get Notified",
        heroTitle: 'The Smart Health Assistant<span class="block text-blue-500 mt-2">for Your Loved Ones</span>',
        heroSubtitle: '<span class="block text-balance hero-subtext-primary">Helma AI empowers elderly individuals with a conversational AI companion so they can live safer, healthier, and more independent lives.</span><span class="block mt-6 text-balance hero-subtext-secondary"> It carefully monitors daily routines, notifies loved ones when support is needed, and delivers <span class="font-semibold text-blue-400">personalized recommendations</span> that continually elevate wellbeing.</span>',
        heroCta: "Discover More",
        featuresTitle: "Our Comprehensive Solutions",
        featuresSubtitle: "Innovative features that simplify daily life, enhance security, and strengthen social bonds.",
        feature1Title: "AI Companion Support",
        feature1Desc: "Understands emotional state during video check-ins, holds natural conversations, and offers compassionate guidance.",
        feature2Title: "Instant Video Check-Ins",
        feature2Desc: "Launches HD video calls with loved ones and caregivers in a single tap for secure, reliable communication.",
        feature3Title: "Medication & Hydration Reminders",
        feature3Desc: "Delivers personalized medication and water alerts that reinforce healthy daily habits.",
        feature4Title: "Exercise Recommendations",
        feature4Desc: "Suggests gentle daily movement and stretching routines tailored to individual mobility.",
        feature5Title: "Weather & News Briefings",
        feature5Desc: "Presents concise weather updates and daily news summaries in an easy-to-follow feed.",
        feature6Title: "Emergency & Voice Support",
        feature6Desc: "Combines an SOS button with voice-triggered help requests for instant assistance.",
        feature7Title: "Cognitive Activities",
        feature7Desc: "Keeps minds sharp with daily puzzles, memory games, and engaging conversational tasks.",
        feature8Title: "Personal Routine Detection",
        feature8Desc: "Learns habits to deliver timely suggestions and reminders throughout the day.",
        feature9Title: "Weekly Health Reports",
        feature9Desc: "Compiles wellbeing and activity insights into shareable reports for family members.",
        feature10Title: "Emotion-Aware Encouragement",
        feature10Desc: "Monitors speech and facial expressions to send uplifting, personalized support messages.",
        teamTitle: "Project Team",
        teamSubtitle: 'A five-member team of computer engineering students united by a vision<br class="hidden sm:block">to use technology for social benefit.',
        teamMember1Name: "Ulaş UÇRAK",
        teamMember1Role: "Project Manager & AI Developer",
        teamMember1Desc: "Leads model development, owns the roadmap, and keeps collaboration on track.",
        teamMember2Name: "Arda YILDIZ",
        teamMember2Role: "Mobile Developer (iOS & Android)",
        teamMember2Desc: "Optimizes the cross-platform app experience, ensuring speed and reliability.",
        teamMember3Name: "Barkın SARIKARTAL",
        teamMember3Role: "Research & Integration",
        teamMember3Desc: "Explores emerging tech, plans integrations, and keeps external services aligned.",
        teamMember4Name: "Doğukan POYRAZ",
        teamMember4Role: "Backend & Database Developer",
        teamMember4Desc: "Builds the server architecture, data pipelines, and secure storage layers.",
        teamMember5Name: "Umut Eray AÇIKGÖZ",
        teamMember5Role: "AI Developer",
        teamMember5Desc: "Designs pipeline and fusion processes of developed models.",
        contactTitle: "Stay Updated on Our Progress!",
        contactSubtitle: "Sign up for our email list to be the first to know when the Helma AI app is released.",
        emailPlaceholder: "Your email address",
        subscribeButton: "Sign Up",
        formSubmitting: "Submitting…",
        formSuccess: "Successfully subscribed! Thank you.",
        formErrorInvalid: "Please enter a valid email address.",
        formErrorDuplicate: "This email address is already on our list.",
        formErrorServer: "A server error occurred. Please try again later.",
        formErrorGeneric: "Something went wrong. Please try again.",
        footerSlogan: "Improving the quality of life for the elderly with technology.",
        footerFollow: "Follow Us",
        footerRights: "&copy; 2025 Helma AI. All rights reserved.",
    }
};

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    // --- Language & Theme Management ---
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    
    const langToggle = document.getElementById('lang-toggle');
    let currentLang = localStorage.getItem('lang') || 'tr';
    let currentTheme = localStorage.getItem('theme') || 'dark';

    const inlineThemeIcons = {
        light: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="block h-5 w-5 transition-transform duration-200">
                    <circle cx="12" cy="12" r="4"></circle>
                    <path d="M12 2v2"></path>
                    <path d="M12 20v2"></path>
                    <path d="m4.93 4.93 1.41 1.41"></path>
                    <path d="m17.66 17.66 1.41 1.41"></path>
                    <path d="M2 12h2"></path>
                    <path d="M20 12h2"></path>
                    <path d="m6.34 17.66-1.41 1.41"></path>
                    <path d="m19.07 4.93-1.41 1.41"></path>
                </svg>`,
        dark: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="block h-5 w-5 transition-transform duration-200">
                    <path d="M12 3a9 9 0 0 0 9 9 7 7 0 0 1-7 7 9 9 0 0 1 0-18"></path>
               </svg>`
    };

    const setLanguage = (lang) => {
        currentLang = lang;
        localStorage.setItem('lang', lang);
        langToggle.textContent = lang === 'tr' ? 'TR' : 'EN';
        document.documentElement.lang = lang;

        document.querySelectorAll('[data-lang-key]').forEach(el => {
            const key = el.getAttribute('data-lang-key');
            const translation = translations[lang][key];
            if (translation) {
                if (el.hasAttribute('placeholder')) {
                    el.setAttribute('placeholder', translation);
                } else {
                    el.innerHTML = translation;
                }
            }
        });
    };

    const updateThemeIcon = (theme) => {
        if (!themeIcon) return;
        themeIcon.innerHTML = theme === 'light' ? inlineThemeIcons.light : inlineThemeIcons.dark;
    };

    const setTheme = (theme) => {
        currentTheme = theme;
        localStorage.setItem('theme', theme);
        if (theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }
        updateThemeIcon(theme);
    };

    langToggle.addEventListener('click', () => {
        setLanguage(currentLang === 'tr' ? 'en' : 'tr');
    });

    themeToggle.addEventListener('click', () => {
        setTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    // --- Mobile Menu ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    mobileMenuButton.addEventListener('click', () => {
        const isHidden = mobileMenu.classList.toggle('hidden');
        const icon = mobileMenuButton.querySelector('i');
        icon.setAttribute('data-lucide', isHidden ? 'menu' : 'x');
        lucide.createIcons();
    });

    document.querySelectorAll('#mobile-menu a, #header a').forEach(link => {
        link.addEventListener('click', (e) => {
            if (e.currentTarget.getAttribute('href').startsWith('#')) {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.querySelector('i').setAttribute('data-lucide', 'menu');
                lucide.createIcons();
            }
        });
    });

    // --- Contact Form ---
    const contactForm = document.getElementById('contact-form');

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Formun normal gönderimini engelle

        // Değişkenleri butona tıklandığı anda tanımlıyoruz
        const emailInput = document.getElementById('email-input');
        const formMessage = document.getElementById('form-message');
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const emailValue = emailInput.value;
        const originalButtonText = translations[currentLang].subscribeButton || 'Kaydol';

        // Butonu devre dışı bırak ve kullanıcıya bilgi ver
        submitButton.disabled = true;
        submitButton.textContent = translations[currentLang].formSubmitting || 'Kaydediliyor...';
        formMessage.textContent = '';
        formMessage.classList.remove('text-green-500', 'text-red-500');

        try {
            // Cloud Function'ı çağır
            const subscribeFunction = functions.httpsCallable('subscribeToList');
            const result = await subscribeFunction({ email: emailValue });

            // Başarılı olursa
            formMessage.textContent = translations[currentLang].formSuccess || 'Başarıyla kaydoldunuz! Teşekkür ederiz.';
            formMessage.classList.add('text-green-500');
            emailInput.value = ''; // Input'u temizle

        } catch (error) {
            console.error('Fonksiyon hatası:', error);
            const errorCode = error.code || '';
            let errorKey = 'formErrorGeneric';

            if (errorCode.includes('invalid-argument')) {
                errorKey = 'formErrorInvalid';
            } else if (errorCode.includes('already-exists')) {
                errorKey = 'formErrorDuplicate';
            } else if (errorCode.includes('internal')) {
                errorKey = 'formErrorServer';
            }

            formMessage.textContent = translations[currentLang][errorKey] || translations[currentLang].formErrorGeneric;
            formMessage.classList.add('text-red-500');
        } finally {
            // Her durumda butonu tekrar aktif et
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
    
    // --- Scrollspy & Header Style ---
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (pageYOffset >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes(current)) {
                link.classList.add('active');
            }
        });
        
        const header = document.getElementById('header');
        if (window.scrollY > 50) {
            header.classList.add('bg-opacity-80');
        } else {
            header.classList.remove('bg-opacity-80');
        }
    });

    // --- Initial Load ---
    setTheme(currentTheme);
    setLanguage(currentLang);
});