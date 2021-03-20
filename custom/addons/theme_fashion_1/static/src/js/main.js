(function ($) {

	"use strict";

	// Sticky nav
	var $headerStick = $('.Sticky');
	$(window).on("scroll", function () {
		if ($(this).scrollTop() > 80) {
			$headerStick.addClass("sticky_element");
		} else {
			$headerStick.removeClass("sticky_element");
		};
	});

	// Menu Categories
	$(window).resize(function () {
		if ($(window).width() >= 768) {
			$('a[href="#menu"]').on('click', function (e) {
				e.preventDefault();
			});
			$('.categories').addClass('menu');
			$('.menu ul > li').on('mouseover', function (e) {
				$(this).find("ul:first").show();
				$(this).find('> span a').addClass('active');
			}).on('mouseout', function (e) {
				$(this).find("ul:first").hide();
				$(this).find('> span a').removeClass('active');
			});
			$('.menu ul li li').on('mouseover', function (e) {
				if ($(this).has('ul').length) {
					$(this).parent().addClass('expanded');
				}
				$('.menu ul:first', this).parent().find('> span a').addClass('active');
				$('.menu ul:first', this).show();
			}).on('mouseout', function (e) {
				$(this).parent().removeClass('expanded');
				$('.menu ul:first', this).parent().find('> span a').removeClass('active');
				$('.menu ul:first', this).hide();
			});
		} else {
			$('.categories').removeClass('menu');
		}
	}).resize();

	// Mobile Mmenu
	var $menu = $("#menu").mmenu({
		"extensions": ["pagedim-black"],
		counters: true,
		keyboardNavigation: {
			enable: true,
			enhance: true
		},
		navbar: {
			title: 'MENU'
		},
		offCanvas: {
		  pageSelector: "#page"
	   },
		navbars: [{position:'bottom',content: ['']}]},
		{
		// configuration
		clone: true,
		classNames: {
			fixedElements: {
				fixed: "menu_fixed"
			}
		}
	});

	// Menu
	$('a.open_close').on("click", function () {
		$('.main-menu').toggleClass('show');
		$('.layer').toggleClass('layer-is-visible');
	});
	$('a.show-submenu').on("click", function () {
		$(this).next().toggleClass("show_normal");
	});
	$('a.show-submenu-mega').on("click", function () {
		$(this).next().toggleClass("show_mega");
	});

	$('a.btn_search_mob').on("click", function () {
		$('.search_mob_wp').slideToggle("fast");
	});


	/* Cart dropdown */
	$('.dropdown-access').hover(function () {
		$(this).find('.dropdown-menu').stop(true, true).delay(50).fadeIn(300);
	}, function () {
		$(this).find('.dropdown-menu').stop(true, true).delay(50).fadeOut(300);
	});

	/* Cart Dropdown Hidden From tablet */
	$(window).bind('load resize', function () {
		var width = $(window).width();
		if (width <= 768) {
			$(' a.access_link').removeAttr("data-toggle", "dropdown")
		} else {
			$('a.access_link').attr("data-toggle", "dropdown")
		}
	});

	// Top panel on click: add to cart, search header
	var $topPnl = $('.top_panel');
	var $pnlMsk = $('.layer');

	$('.btn_add_to_cart a').on('click', function(){
		$topPnl.addClass('show');
		$pnlMsk.addClass('layer-is-visible');
	});
	$('a.search_panel').on('click', function(){
		$topPnl.addClass('show');
		$pnlMsk.addClass('layer-is-visible');
	});
	$('a.btn_close_top_panel').on('click', function(){
		$topPnl.removeClass('show');
		$pnlMsk.removeClass('layer-is-visible');
	});

	//Footer collapse
	var $headingFooter = $('footer h3');
	$(window).resize(function() {
        if($(window).width() <= 768) {
      		$headingFooter.attr("data-toggle","collapse");
        } else {
          $headingFooter.removeAttr("data-toggle","collapse");
        }
    }).resize();
	$headingFooter.on("click", function () {
		$(this).toggleClass('opened');
	});

	/* Footer reveal */
	if ($(window).width() >= 1024) {
		$('footer.revealed').footerReveal({
		shadow: false,
		opacity:0.6,
		zIndex: 1
	});
	};

	// Scroll to top
	var pxShow = 800; // height on which the button will show
	var scrollSpeed = 500; // how slow / fast you want the button to scroll to top.
	$(window).scroll(function(){
	 if($(window).scrollTop() >= pxShow){
		$("#toTop").addClass('visible');
	 } else {
		$("#toTop").removeClass('visible');
	 }
	});
	$('#toTop').on('click', function(){
	 $('html, body').animate({scrollTop:0}, scrollSpeed);
	 return false;
	});

	// Tooltip
	$(window).resize(function() {
        if($(window).width() <= 768) {
      		$('.tooltip-1').tooltip('disable');
        } else {
         $('.tooltip-1').tooltip({html: true});
        }
    }).resize();

})(window.jQuery); 
