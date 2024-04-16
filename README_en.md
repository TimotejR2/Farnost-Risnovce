# Farnost-Risnovce

## Introduction

This repository contains the source code for the [risnovcefara.sk](https://risnovcefara.sk) website. The website offers basic functionalities such as adding posts, logging in, and more. It is primarily designed for deployment on a Vercel server.

## Requirements

This project requires the following:

- Python 3.8+
- PostgreSQL
- Flask
- Werkzeug
- psycopg2

## Installation and Usage

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

To start the application, use the Flask run command:

```bash
flask run
```

## Vercel and Remote Database

This project uses a remote database hosted on Vercel. To connect to the remote database, use the `POSTGRES_URL` environment variable or create a `postgres.sql` file in the config folder and paste the URL there.

For more information, see the [Vercel documentation](https://vercel.com/docs/storage/vercel-postgres).

## License

This project is licensed under the GPL-3.0 License.

## Author

This project was created by [Timotej Ružička](https://github.com/TimotejR2).

## Using the Code

Feel free to modify this code according to your needs. If you need help, don't hesitate to contact me at [timotej.ruzicka@gmail.com](mailto:timotej.ruzicka@gmail.com). If you find this project useful, please consider giving it a star and following me on GitHub.

## Contributions

This project is still under development. Any contributions to the project would be greatly appreciated. Thank you!