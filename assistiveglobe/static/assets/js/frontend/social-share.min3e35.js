document.addEventListener("click",(function(t){const e=t.target.closest(".wpex-social-share__link, .vcex-social-share__button");if(!e)return;const a=e.closest(".wpex-social-share, .vcex-social-share"),s=e.classList,r=a.dataset.url,i=e.dataset.target;let n=a.dataset.specs||"",o=a.dataset.title,c="";switch(!0){case s.contains("wpex-twitter"):a.dataset.twitterTitle&&(o=a.dataset.twitterTitle),c=`https://twitter.com/intent/tweet?text=${o}&url=${r}`,a.dataset.twitterHandle&&(c+=`&via=${a.dataset.twitterHandle}`);break;case s.contains("wpex-facebook"):c=`https://www.facebook.com/sharer/sharer.php?u=${r}`;break;case s.contains("wpex-pinterest"):c=`https://www.pinterest.com/pin/create/button/?url=${r}`,a.dataset.image&&(c+=`&media=${a.dataset.image}`),a.dataset.summary&&(c+=`&description=${a.dataset.summary}`);break;case s.contains("wpex-linkedin"):c=`https://www.linkedin.com/shareArticle?mini=true&url=${r}&title=${o}`,a.dataset.summary&&(c+=`&summary=${a.dataset.summary}`),a.dataset.source&&(c+=`&source=${a.dataset.source}`);break;case s.contains("wpex-reddit"):c=`https://www.reddit.com/submit?url=${r}&title=${o}`;break;case s.contains("wpex-whatsapp"):c=`https://wa.me/?text=${r}`;break;case s.contains("wpex-print"):return t.preventDefault(),t.stopPropagation(),window.print();case s.contains("wpex-email"):return c=`mailto:?subject=${a.dataset.emailSubject}&body=${a.dataset.emailBody}`,window.location.href=c,t.preventDefault(),void t.stopPropagation();case s.contains("wpex-telegram"):c=`https://t.me/share/url?url=${r}&text=${o}`;break;default:c=e.getAttribute("href"),n=""}c&&(window.open(c,i,n).focus(),t.preventDefault(),t.stopPropagation())}));