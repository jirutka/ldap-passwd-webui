<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow">

    <title>{{ page_title }}</title>

    <link rel="stylesheet" href="{{ url('static', filename='style.css') }}">
  </head>

  <body>
    <main>
      <h1>{{ page_title }}</h1>

      <form method="post">
        <label for="username">Username</label>
        <input id="username" name="username" value="{{ get('username', '') }}" type="text" required autofocus>

        <label for="old-password">Old password</label>
        <input id="old-password" name="old-password" type="password" required>

        <label for="new-password">New password</label>
        <input id="new-password" name="new-password" type="password"
            pattern=".{8,}" oninvalid="SetCustomValidity('Password must be at least 8 characters long.')" required>

        <label for="confirm-password">Confirm new password</label>
        <input id="confirm-password" name="confirm-password" type="password"
            pattern=".{8,}" oninvalid="SetCustomValidity('Password must be at least 8 characters long.')" required>

        <button type="submit">Update password</button>
      </form>

      <div class="alerts">
        %for type, text in get('alerts', []):
          <div class="alert {{ type }}">{{ text }}</div>
        %end
      </div>
    </main>
  </body>
</html>
