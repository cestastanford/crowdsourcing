---
layout: front
title: Crowdsourcing
project-name: crowdsourcing
---

<div class="row">

    <div class="col-md-8">
    <h2>News and Updates</h2>
      <div class="news">
        {% for post in site.categories.news %}
        <div class="article">
        <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
        <p>{{ post.date }}</p>
        <p>{{ post.content }}</p>

        </div>
        {% endfor %}
      </div>
    </div>

    <div class="col-md-4">
    <h2>Upcoming Events</h2>
    <ul class="events">
    {% for post in site.categories.event %}
      <li><a href="{{ post.url }}">{{ post.title }}</a></li>
    {% endfor %}
    </ul>
    </div>

</div>
