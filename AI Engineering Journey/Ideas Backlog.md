# Ideas Backlog

## Feature
Merchandise Locations

### Why
Help users find official merchandise stands during an event.

### Challenges
The location changes depending on the venue, artist, and event.

### Possible Solution
Integrate a reliable venue data source instead of relying only on the LLM.

### Risk
Avoid hallucinations by not guessing merchandise locations.

Review unsupported general advice in Food section.

### Ticket / Package Information

- Identify the user's ticket or VIP package.
- Show what is included in the specific package.
- Check for benefits such as soundcheck, early entry, VIP check-in, exclusive merchandise, and other package-specific perks.
- Do not assume that all VIP packages include the same benefits.
- Use confirmed package information only.

- Venue Review

## Community Live Updates

Description

Allow attendees of the same event to share real-time updates (e.g., entrance lines, merchandise availability, food wait times, transportation, venue information).

Goal

Improve the event experience through community-generated, real-time information.

Potential AI Features

Summarize live updates.
Group similar reports.
Highlight the most relevant information.
Filter outdated or duplicate updates.
Detect spam or irrelevant messages.

Possible MVP

Instead of a full chat, allow users to submit short event updates that are automatically organized into categories.

Examples:

🚪 Entrance
👕 Merchandise
🍔 Food & Drinks
🚻 Restrooms
🚆 Transportation
ℹ️ General

Reason for backlog: This feature requires real-time infrastructure, moderation, and user management. It is intentionally postponed until after Version 1.0.

Hoje, assim que encontra o artista, ela testa aquele evento e pode retornar mismatch imediatamente.

Exemplo futuro:

Bon Jovi → MSG
Bon Jovi → Boston
Bon Jovi → Philadelphia

Se o usuário escolher Boston mas o primeiro Bon Jovi encontrado no JSON for MSG, o código pode acusar venue errado antes de chegar ao segundo registro.

Para o banco atual provavelmente não quebra nada, porque cadastramos poucos eventos. Mas isso é uma dívida técnica real.

Informações sobre freebies e principalmente na comunidade

Colocar lightstick na nova do kpop ou fazer um proprio nosso

Quando Nova comprimentar o fa chama-lo pelo nome: tipo stays, atinny etc.

O que pode chamar atenção das companhias 


