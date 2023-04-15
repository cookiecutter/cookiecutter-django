# Contributors

## Core Developers

These contributors have commit flags for the repository, and are able to
accept and merge pull requests.

<table>
  <tr>
    <th>Name</th>
    <th>Github</th>
    <th>Twitter</th>
  </tr>
  {%- for contributor in core_contributors %}
  <tr>
    <td>{{ contributor.name }}</td>
    <td>
      <a href="https://github.com/{{ contributor.github_login }}">{{ contributor.github_login }}</a>
    </td>
    <td>{{ contributor.twitter_username }}</td>
  </tr>
  {%- endfor %}
</table>

_Audrey is also the creator of Cookiecutter. Audrey and Daniel are on
the Cookiecutter core team._

## Other Contributors

Listed in alphabetical order.

<table>
  <tr>
    <th>Name</th>
    <th>Github</th>
    <th>Twitter</th>
  </tr>
  {%- for contributor in other_contributors %}
  <tr>
    <td>{{ contributor.name }}</td>
    <td>
      <a href="https://github.com/{{ contributor.github_login }}">{{ contributor.github_login }}</a>
    </td>
    <td>{{ contributor.twitter_username }}</td>
  </tr>
  {%- endfor %}
</table>

### Special Thanks

The following haven't provided code directly, but have provided
guidance and advice.

- Jannis Leidel
- Nate Aune
- Barry Morrison
