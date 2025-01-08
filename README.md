# Reddit Realtime Keyword Search

## Overview
This project is a real-time solution for browsing specific subreddits on Reddit and filtering posts that contain certain keywords. The product is inspired by tools like GummySearch and leverages the Reddit API to deliver precise and efficient results.

## Features
- **Subreddit Browsing**: Navigate through specific subreddits of your choice.
- **Keyword Filtering**: Retrieve posts that include defined keywords in titles, bodies, or comments.
- **Real-Time Updates**: Fetch and display posts in real-time, ensuring the latest content is always accessible.
- **Customizable Search**: Allow users to specify multiple subreddits and keywords for a personalized experience.

## Technologies Used
- **Programming Language**: Python
- **Libraries**: PRAW (Python Reddit API Wrapper)

## Prerequisites
- Python (v3.8+)
- Reddit API credentials (client ID, client secret, username, password, and user agent)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/reddit-realtime-solution.git
   cd reddit-realtime-solution
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```env
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   ```.


## Contributing
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add feature-name'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Inspired by GummySearch for the core idea.
- Thanks to Reddit for providing a robust API for developers.

