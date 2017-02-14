$(document).ready(function() {
  $cardTemplate = $("#card-template").children();
  $cardsContainer = $("#cards-container");
  $loadMoreBtn = $("#load-more-btn");
  $hashtagBtn = $("#hashtag-btn");
  $hashtagInput = $("#hashtag-input");
  $maxIdInput = $("#max-id");

  $loadMoreBtn.click(function() {
    hashtag = $hashtagInput.val();
    maxId = $maxIdInput.val().trim();
    $loadMoreBtn.addClass("loading");

    searchTweets(hashtag, maxId, function(data) {
      console.log(data);
      cards = createCards(data.tweets);
      $cardsContainer.append(cards.join(""));
      $maxIdInput.val(data.meta.maxId);
    }, function() {
      $loadMoreBtn.removeClass("loading");
    });
  });

  $hashtagBtn.click(function() {
    hashtag = $hashtagInput.val();
    $hashtagBtn.addClass("loading");

    searchTweets(hashtag, null, function(data) {
      console.log(data);
      cards = createCards(data.tweets);
      $cardsContainer.html(cards.join(""));
      $maxIdInput.val(data.meta.maxId);
    }, function() {
      $hashtagBtn.removeClass("loading");
    });
  });

  function searchTweets(hashtag, maxId, doneCb, alwaysCb) {
    data = { hashtag: hashtag, 'max_id': maxId };

    $.ajax({
      dataType: "json",
      url: "/api",
      data: data,
      timeout: 10000
    }).done(doneCb)
      .fail(function(data) {
        console.log(data);
        console.log(data.responseJSON);
        console.log('Something went wrong');
      })
      .always(alwaysCb);
  }

  function createCards(cardsData) {
    cards = [];
    $.each(cardsData, function(key, tweet) {
      cards.push(createCard(tweet));
    });

    return cards;
  }

  function createCard(tweet) {
    $card = $cardTemplate.clone();
    $card.find(".header").text(tweet.user);
    $card.find(".meta").text(tweet.date);
    $card.find(".description").text(tweet.text);
    $card.find(".retweet-count").text(tweet.retweetCount);

    return $card[0].outerHTML;
  }
});
