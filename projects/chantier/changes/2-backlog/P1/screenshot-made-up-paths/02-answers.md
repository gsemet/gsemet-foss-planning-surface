# Answers

## paths-Q1: rule and check

2026-11-17, the user chose the recommended answer: the Driver and Verifier cards require made-up paths and no username in any image, and an explicit check before every upload to the forge: the agent looks at the image for the user's username and home folder, and uploads only once neither shows.

Spec critic: yes, it changes two roles' cards and what may reach the forge.

## Spec questions (2026-11-17)

- paths-Q2 (the user's own screenshot shows the username or home folder): the Driver does not upload it, keeps the Known gap, says why in a `note` and in its hand-back; the Chief of Staff asks the user for a new one with made-up paths.
- paths-Q3 (images in the planning folder): yes, every image a Driver or Verifier keeps in the planning folder (pushed to GitHub with the planning surface) follows the made-up-path rule and gets the same look before it is kept; this covers the QA driver's `evidence/` and the release Driver's `work/` captures. Cleaning up images already committed (CR-305's) stays out of scope; the user leaves them as they are.
- paths-Q4 (a leak found after upload, on the description pass): the Driver replaces the image with a clean capture, says in a `note` and in its hand-back that the old one was uploaded, and the Chief of Staff tells the user.
