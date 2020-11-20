#!/bin/bash

_is_sourced() {
	# https://unix.stackexchange.com/a/215279
	[ "${#FUNCNAME[@]}" -ge 2 ] \
		&& [ "${FUNCNAME[0]}" = '_is_sourced' ] \
		&& [ "${FUNCNAME[1]}" = 'source' ]
}

run_manage() {
  python -m manage "$@"
}

createsuperuser() {
  if [ "$USERNAME" ] && [ "$PASSWORD" ] && [ "$EMAIL" ]; then
    export DJANGO_SUPERUSER_USER=$USERNAME
    export DJANGO_SUPERUSER_PASSWORD=$PASSWORD
    export DJANGO_SUPERUSER_EMAIL=$EMAIL
  else
    export DJANGO_SUPERUSER_USER=admin
    export DJANGO_SUPERUSER_PASSWORD=admin
    export DJANGO_SUPERUSER_EMAIL=admin@noreply.com
  fi
  run_manage createsuperuser \
    --username=$DJANGO_SUPERUSER_USER \
    --email=$DJANGO_SUPERUSER_EMAIL --no-input
}

init() {
  run_manage makemigrations
  run_manage migrate
}

_main() {
  if [ "$1" = 'start' ]; then
    python manage.py runserver 0:8000
  elif [ "$1" = 'init' ]; then
    init
  elif [ "$1" = 'createsuperuser' ]; then
    createsuperuser
  fi
}

if ! _is_sourced; then
	_main "$@"
fi
