/**
 * AdminLTE Demo Menu
 * ------------------
 * You should not use this file in production.
 * This file is for demo purposes only.
 */

/* eslint-disable camelcase */

(function ($) {
  'use strict'

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1)
  }

  function createSkinBlock(colors, callback, noneSelected) {
    var $block = $('<select />', {
      class: noneSelected ? 'custom-select mb-3 border-0' : 'custom-select mb-3 text-light border-0 ' + colors[0].replace(/accent-|navbar-/, 'bg-')
    })

    if (noneSelected) {
      var $default = $('<option />', {
        text: 'None Selected'
      })
      if (callback) {
        $default.on('click', callback)
      }

      $block.append($default)
    }

    colors.forEach(function (color) {
      var $color = $('<option />', {
        class: (typeof color === 'object' ? color.join(' ') : color).replace('navbar-', 'bg-').replace('accent-', 'bg-'),
        text: capitalizeFirstLetter((typeof color === 'object' ? color.join(' ') : color).replace(/navbar-|accent-|bg-/, '').replace('-', ' '))
      })

      $block.append($color)

      $color.data('color', color)

      if (callback) {
        $color.on('click', callback)
      }
    })

    return $block
  }

  var $sidebar = $('.control-sidebar')
  var $container = $('<div />', {
    class: 'p-3 control-sidebar-content'
  })

  $sidebar.append($container)

  // Checkboxes

  $container.append(
    '<h5>Customize AdminLTE</h5><hr class="mb-2"/>'
  )

  var $dark_mode_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('dark-mode'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('dark-mode')
    } else {
      $('body').removeClass('dark-mode')
    }
  })
  var $dark_mode_container = $('<div />', { class: 'mb-4' }).append($dark_mode_checkbox).append('<span>Dark Mode</span>')
  $container.append($dark_mode_container)

  $container.append('<h6>Header Options</h6>')
  var $header_fixed_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('layout-navbar-fixed'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('layout-navbar-fixed')
    } else {
      $('body').removeClass('layout-navbar-fixed')
    }
  })
  var $header_fixed_container = $('<div />', { class: 'mb-1' }).append($header_fixed_checkbox).append('<span>Fixed</span>')
  $container.append($header_fixed_container)

  var $dropdown_legacy_offset_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('.main-header').hasClass('dropdown-legacy'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('.main-header').addClass('dropdown-legacy')
    } else {
      $('.main-header').removeClass('dropdown-legacy')
    }
  })
  var $dropdown_legacy_offset_container = $('<div />', { class: 'mb-1' }).append($dropdown_legacy_offset_checkbox).append('<span>Dropdown Legacy Offset</span>')
  $container.append($dropdown_legacy_offset_container)

  var $no_border_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('.main-header').hasClass('border-bottom-0'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('.main-header').addClass('border-bottom-0')
    } else {
      $('.main-header').removeClass('border-bottom-0')
    }
  })
  var $no_border_container = $('<div />', { class: 'mb-4' }).append($no_border_checkbox).append('<span>No border</span>')
  $container.append($no_border_container)

  $container.append('<h6>Sidebar Options</h6>')

  var $sidebar_collapsed_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('sidebar-collapse'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('sidebar-collapse')
      $(window).trigger('resize')
    } else {
      $('body').removeClass('sidebar-collapse')
      $(window).trigger('resize')
    }
  })
  var $sidebar_collapsed_container = $('<div />', { class: 'mb-1' }).append($sidebar_collapsed_checkbox).append('<span>Collapsed</span>')
  $container.append($sidebar_collapsed_container)

  $(document).on('collapsed.lte.pushmenu', '[data-widget="pushmenu"]', function () {
    $sidebar_collapsed_checkbox.prop('checked', true)
  })
  $(document).on('shown.lte.pushmenu', '[data-widget="pushmenu"]', function () {
    $sidebar_collapsed_checkbox.prop('checked', false)
  })

  var $sidebar_fixed_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('layout-fixed'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('layout-fixed')
      $(window).trigger('resize')
    } else {
      $('body').removeClass('layout-fixed')
      $(window).trigger('resize')
    }
  })
  var $sidebar_fixed_container = $('<div />', { class: 'mb-1' }).append($sidebar_fixed_checkbox).append('<span>Fixed</span>')
  $container.append($sidebar_fixed_container)

  var $sidebar_mini_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('sidebar-mini'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('sidebar-mini')
    } else {
      $('body').removeClass('sidebar-mini')
    }
  })
  var $sidebar_mini_container = $('<div />', { class: 'mb-1' }).append($sidebar_mini_checkbox).append('<span>Mini</span>')
  $container.append($sidebar_mini_container)

  var $sidebar_mini_md_checkbox = $('<input />', {
    type: 'checkbox',
    value: 1,
    checked: $('body').hasClass('sidebar-mini-md'),
    class: 'mr-1'
  }).on('click', function () {
    if ($(this).is(':checked')) {
      $('body').addClass('sidebar-mini-md')
    } else {
      $('body').removeClass('sidebar-mini-md')
    }
  })
  var $sidebar_mini_md_container = $('<div />', { class: 'mb-4' }).append($sidebar_mini_md_checkbox).append('<span>Mini MD</span>')
  $container.append($sidebar_mini_md_container)

  $container.append('<h6>Colors</h6>')

  var $accent_colors = createSkinBlock(
    ['accent-primary', 'accent-warning', 'accent-info', 'accent-danger', 'accent-success'],
    function () {
      var color = $(this).data('color')
      var accent_class = $('body').data('accent-color')

      $('body').removeClass(accent_class)
      $('body').addClass(color)
      $('body').data('accent-color', color)
    }
  )
  var $navbar_colors = createSkinBlock(
    ['navbar-primary', 'navbar-warning', 'navbar-info', 'navbar-danger', 'navbar-success'],
    function () {
      var color = $(this).data('color')
      var navbar_class = $('body').data('navbar-color')

      $('body').removeClass(navbar_class)
      $('body').addClass(color)
      $('body').data('navbar-color', color)
    }
  )

  $container.append($accent_colors)
  $container.append($navbar_colors)

  $container.append('<h6>Dark Sidebar Variants</h6>')

  var $dark_accent_colors = createSkinBlock(
    ['navbar-dark navbar-accent-primary', 'navbar-dark navbar-accent-warning', 'navbar-dark navbar-accent-info', 'navbar-dark navbar-accent-danger', 'navbar-dark navbar-accent-success'],
    function () {
      var color = $(this).data('color')
      var navbar_class = $('body').data('navbar-color')

      $('body').removeClass(navbar_class)
      $('body').addClass(color)
      $('body').data('navbar-color', color)
    }
  )
  var $dark_navbar_colors = createSkinBlock(
    ['dark accent-primary', 'dark accent-warning', 'dark accent-info', 'dark accent-danger', 'dark accent-success'],
    function () {
      var color = $(this).data('color')
      var accent_class = $('body').data('accent-color')

      $('body').removeClass(accent_class)
      $('body').addClass(color)
      $('body').data('accent-color', color)
    }
  )

  $container.append($dark_accent_colors)
  $container.append($dark_navbar_colors)
})(jQuery)
