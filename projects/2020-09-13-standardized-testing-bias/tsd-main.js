/**
 * When tsd-callouts are overlapping, makes it a bit easier for the reader --
 * a given callout will go to the top if it is navigated to through a button,
 * or if it is clicked on by the reader.
 */
$(function() {
  $(".arrow").click(function(e) {
    e.stopPropagation();
    $(".arrow").css("z-index", 1);
    $($(this).attr("href")).css("z-index", 99);
  });
  $(".tsd-callout").click(function() {
    $(".tsd-callout").css("z-index", 1);
    $(this).css("z-index", 99);
  })
})