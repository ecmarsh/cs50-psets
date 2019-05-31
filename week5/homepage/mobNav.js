var mobNav = document.querySelector('aside');
var buttonOpen = document.querySelector('#open').addEventListener('click', function (e) {
	if (mobNav) {
		mobNav.classList.add('mobile-nav--active');
	}
});
var buttonClose = document.querySelector('#close').addEventListener('click', function (e) {
	mobNav.classList.remove('mobile-nav--active');
});