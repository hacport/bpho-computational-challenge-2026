# Putting this project on GitHub

Everything is prepared — `.gitignore`, `README.md` and `LICENSE` are written and
git is initialised with your name and email. You just need to run the commands,
because pushing requires *your* GitHub login, which I can't do for you.

Pick **Route A** (proper git, worth learning) or **Route B** (drag and drop, 5
minutes, no terminal).

---

## Route A — git (recommended)

### 1. Make the empty repo on GitHub

Go to [github.com/new](https://github.com/new) and set:

- **Repository name:** `bpho-computational-challenge-2026`
- **Description:** `Ten quantum mechanics models in Python — BPhO Computational Challenge 2026`
- **Public**
- **Do NOT tick** "Add a README", "Add .gitignore" or "Choose a licence" —
  you already have all three. Ticking them causes a merge conflict on your
  first push.

Click **Create repository**.

### 2. Run these in PowerShell

Open PowerShell in the project folder (in File Explorer: click the address bar,
type `powershell`, press Enter). Then paste this whole block — it's already set
up for your account (`hacport`):

```powershell
cd "$HOME\OneDrive\Desktop\BPhO_ComPhys_Challenge_2026"

git add -A
git commit -m "BPhO Computational Challenge 2026: ten quantum mechanics models"
git branch -M main
git remote add origin https://github.com/hacport/bpho-computational-challenge-2026.git
git push -u origin main
```

A browser window will open asking you to sign in to GitHub. Do that once and it
remembers — that sign-in is the step nobody can do for you, which is why these
commands are yours to run.

**If `git` is not recognised:** install Git for Windows from
[git-scm.com](https://git-scm.com/download/win), accept every default, close and
reopen PowerShell, then paste the block again.

**If anything else errors:** delete the hidden `.git` folder in the project
directory and run the block again with `git init` added as the first line. The
repository was initialised from my sandbox, which OneDrive partly blocks, so a
clean start on your own machine fixes anything left half-done.

### 3. Check it worked

Refresh your repository page. You should see the README rendered with both
animated gifs playing, and 94 files.

---

## Route B — no terminal

1. Create the repository exactly as in step 1 above, but **do** tick "Add a
   README" this time.
2. On the repo page click **Add file → Upload files**.
3. In File Explorer, select everything in the project folder **except**:
   - `BPhO ComPhys Challenge 2026.pdf`
   - `BPhO CompPhys2026 Quantum.pdf`
   - the `QM problem sheets` folder
   - the `.git` and `__pycache__` folders

   Drag them into the browser window.
4. Scroll down, write `Initial commit`, click **Commit changes**.
5. Click the pencil icon on the README GitHub made, delete its contents, paste
   in the contents of your own `README.md`, and commit.

GitHub's web uploader handles about 100 files at a time, so you may need two
trips — do the loose files first, then the `QM_Course` folder.

---

## Why some files are excluded

The challenge pack (`BPhO CompPhys2026 Quantum.pdf`), the cover document and the
`QM problem sheets` folder are **copyright the British Physics Olympiad and
Dr A. French**. They're free to download from bpho.org.uk, but republishing
someone else's material under your own repository isn't yours to do — so the
README links to the originals instead. That's the normal, correct way to handle
source material, and `.gitignore` already takes care of it.

Everything excluded stays on your computer exactly as it is. Nothing is deleted.

---

## Afterwards

**Add topics** to the repo (the gear icon next to "About"): `physics`,
`python`, `quantum-mechanics`, `simulation`, `numpy`, `matplotlib`,
`computational-physics`. These make it findable.

**Put the link in your YouTube description** and anywhere you list your work —
this is a genuine portfolio piece. A sixth-former with ten verified physics
models and a 22-chapter course they wrote about their own code is not a common
thing to see.

**To update it later**, after changing any file:

```powershell
git add -A
git commit -m "describe what changed"
git push
```

Three commands, every time. That's most of what day-to-day git is.
