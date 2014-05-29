(function() {
    var url;
    var heartbeat = 5*1000;
    var postsEl = document.getElementById('posts');
    var author = window.SHOW_AUTHOR || null;

    var template = Hogan.compile([
        '{{#posts}}',
        '  <div class="well">',
        '    <p>{{ body }}</p>',
        '    <p class="text-right">',
        '      <small>',
        '        At {{ date }}',
        '        by <a href="{{url}}">{{ author }}</a>',
        '      </small>',
        '    </p>',
        '  </div>',
        '{{/posts}}',
    ].join('\n'));

    if (author) {
        url = '/posts?author=' + encodeURIComponent(author);
    } else {
        url = '/posts';
    }

    function renderPosts(posts) {
        var post;
        for (var i = posts.length - 1; i >= 0; i--) {
            post = posts[i];
            post.url = '/author/' + encodeURIComponent(post.author);
        }

        postsEl.innerHTML = template.render({posts: posts})
    }

    function onLoadPosts() {
        if (this.status !== 200) {
            return;
        }

        var data = JSON.parse(this.responseText);
        renderPosts(data.posts);
    }

    function update() {
        request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onload = onLoadPosts;
        request.send();
    }

    function tick() {
        update();
        setTimeout(tick, heartbeat);
    }

    setTimeout(tick, heartbeat);
})()
