$(document).ready(function() {
  $cardTemplate = $("#card-template").children();
  $cardsContainer = $("#cards-container");
  $loadMoreBtn = $("#load-more-btn");
  $hashtagBtn = $("#hashtag-btn");
  $hashtagInput = $("#hashtag-input");
  $maxIdInput = $("#max-id");
  $errorBox = $(".error-box");

  hideError();

  $loadMoreBtn.click(function() {
    hashtag = $hashtagInput.val();
    maxId = $maxIdInput.val().trim();
    $loadMoreBtn.addClass("loading disabled");

    searchTweets(hashtag, maxId, function(data) {
      console.log(data);
      cards = createCards(data.tweets);
      $cardsContainer.append(cards.join(""));
      $maxIdInput.val(data.meta.maxId);
    }, function() {
      $loadMoreBtn.removeClass("loading disabled");
    });
  });

  $hashtagBtn.click(function() {
    hashtag = $hashtagInput.val();
    $hashtagBtn.addClass("loading disabled");

    searchTweets(hashtag, null, function(data) {
      console.log(data);
      cards = createCards(data.tweets);
      $cardsContainer.html(cards.join(""));
      $maxIdInput.val(data.meta.maxId);
    }, function() {
      $hashtagBtn.removeClass("loading disabled");
    });
  });

  function searchTweets(hashtag, maxId, doneCb, alwaysCb) {
    data = { hashtag: hashtag, 'max_id': maxId };
    hideError();

    $.ajax({
      dataType: "json",
      url: "/api",
      data: data,
      timeout: 10000
    }).done(doneCb)
      .fail(function(data) {
        displayError(data.responseJSON.error);
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
    tweetLink = "https://twitter.com/statuses/" + tweet.idStr;
    $card.find(".header").html("<a href='" + tweetLink + "' target='_blank'>" + tweet.user + "</a>");
    $card.find(".meta").text(tweet.date);
    $card.find(".description").text(tweet.text);
    $card.find(".retweet-count").text(tweet.retweetCount);

    return $card[0].outerHTML;
  }

  function displayError(error) {
    $errorBox.find(".msg").html(error.message);
    $errorBox.show();
  }

  function hideError(error) {
    $errorBox.hide();
  }
});
