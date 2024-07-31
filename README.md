<div align="center">
  <a href="#"><img src="/preview.jpg?raw=true"/></a>
</div>

![No Maintained](https://img.shields.io/badge/Maintained%3F-no-red.svg)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/aiogram-2CA5E0?logo=telegram&logoColor=white)

<sup> [:ru: Русская версия README](README_ru.md) </sup>

<sup>Inspired by: [MeowSchool](https://github.com/mironovmeow/MeowSchool)</sup>

## Description
A Telegram bot created to receive notifications about new grades on sh-open.ris61edu.ru (and other similar BARS platforms).

## What's Cool?
- **Dictionary Comparison:** Implemented dictionary comparison.
- **Message Queue:** Solved an issue related to message queuing that I learned about from old Telegram documentation and forums.
- **Code Structure:** This is the first project where I started using a proper code structure. Each function is more or less in its own file (ideally, there should be classes, but I haven't gotten into using them in Python yet).
- **Payment Gateway Integration:** First time integrating the YooKassa payment gateway into a Telegram bot.
- **Legal Documents:** Learned to write a public offer and privacy policy.
- **Psychological Marketing:** Used psychological marketing tricks like "trusted by people with red diplomas" and similar strategies. Also, implemented subscription to a news channel, sending messages to an email database, etc.

## What Didn't Work, But I Tried?
- **Referral System:** Almost done but needs more work.
- **Docker Deployment:** Currently requires running three containers instead of one. Still figuring this out (schoolscores-main, schoolscores-messages, schoolscores-scrapper run separately).
- **Two Bots:** Release and beta versions. Submitting a beta request was supposed to be done through the release version settings.

## Interesting Tools Used:
- Obsidian (Trello analog)
- Docker
- MongoDB

## Why the Project Didn't Develop for Long?
- **API Issues:** Incorrect API behavior. If there are two grades on the same date, only the first one is returned.
- **Frequent Technical Work:** Frequent technical maintenance sends the same code as an authorization error. Using the same data was risky because class teachers could randomly change passwords for the entire class, which happened quite often. Therefore, it was impossible to distinguish between a password change and a server technical error.

## What Else Did I Want to Do?
- Grade statistics generation for a user as an image (requires a lot of optimization and resources).
- Broadcasting by categories (specific class, specific school).
- Referral action notifications.
- School region selection.
- Annual and semester grades.
- Admin panel with subscription duration management and forced blocking.

## Will the Project Be Developed Further?
No, I no longer have access to the BARS diary portal.

The project was developed from early 2023 to September 2023. Currently, I realize and see many makeshift solutions and things I would write differently now.

## Bot Screenshots
<div align="center">
  <img src="/example.webp?raw=true"/>
</div>
