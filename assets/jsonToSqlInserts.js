let fs = require('fs');

let data = JSON.parse(fs.readFileSync('data.json'));
let stadiumStatements = [],
    teamStatements = [],
    matchStatements = [],
    stageStatements = [];

function toNULL(value, quoted=false, date=false) {
    if(value == null) {
        return "NULL";
    } else if(quoted) {
        return `"${value}"`;
    } else if(date) {
        return `FROM_UNIXTIME(${value})`;
    } else {
        return value;
    }
}

/* stadiums */
stadiumStatements.push(...data.stadiums.map(stadium => {
    return `INSERT INTO stadiums(id, name, lat, lng, city) VALUES (
        ${toNULL(stadium.id)},
        ${toNULL(stadium.name, true)},
        ${toNULL(stadium.lat)},
        ${toNULL(stadium.lng)},
        ${toNULL(stadium.city, true)});`.replace(/\n/g, '');
}));

/* teams */

function makeTeamFlagUrl(teamIso2) {
    return `https://storage.cloud.google.com/dgc-worldcup-russia-2018.appspot.com/flags/${teamIso2}.svg?organizationId=48621725833`;
}

teamStatements.push(...data.teams.map(team => {
    return `INSERT INTO teams(id, name, iso2, flag_url) VALUES (
        ${team.id},
        ${toNULL(team.name, true)},
        ${toNULL(team.iso2, true)},
        ${toNULL(makeTeamFlagUrl(team.iso2), true)});`.replace(/\n/g, '');
}));

/* stages */
let stages = [];
let stageMapping = {
    groups: {},
    knockout: {}
};

let groupStages = Object.keys(data.groups).map((group, idx) => {
    let id = idx + 1;
    stageMapping['groups'][group] = id;
    return {
        id: id,
        name: `GROUPE ${group.toUpperCase()}`,
        opening_time: 1527804000, // 1st of June 00:00 Paris
        closing_time: 1528840800, // 13th of June 00:00 Paris
    };
});
stages.push(...groupStages);

let knockoutStages = [
    {
        label: 'Huitièmes de finale',
        json_key: 'round_16'
    },
    {
        label: 'Quarts de finale',
        json_key: 'round_8'
    },
    {
        label: 'Demi-finales',
        json_key: 'round_4'
    },
    { // important that finale is before 3rd place match
        label: 'Finale',
        json_key: 'round_2'
    },
    {
        label: 'Petite finale',
        json_key: 'round_2_loser'
    }
].map((entry, idx) => {
    let id = groupStages.length + idx + 1;
    stageMapping['knockout'][entry.json_key] = id;
    return {
        id: id,
        name: entry.label,
        opening_time: 1527804000, // 29th of June 00:00 Paris
        closing_time: null
    };
});
stages.push(...knockoutStages);

stageStatements.push(...stages.map(stage => {
    return `INSERT INTO stages(id, opening_time, closing_time, name) VALUES (
        ${toNULL(stage.id)},
        ${toNULL(stage.opening_time, false, true)},
        ${toNULL(stage.closing_time, false, true)},
        ${toNULL(stage.name, true)});`.replace(/\n/g, '');
}));


/* Matches */
let matches = [],
    groupMatches = [],
    knockoutMatches = [];

function getTimestampFromISODatetime(isoDatetime) {
    let d = new Date(isoDatetime);
    return d.valueOf() / 1000;
}

Object.keys(data.groups).forEach(group => {
    let stage_id = stageMapping['groups'][group];

    groupMatches.push(...data.groups[group].matches.map(match => {
        return {
          id: match.name,
          stage_id: stage_id,
          match_time: getTimestampFromISODatetime(match.date),
          team_1_id: match.home_team,
          team_2_id: match.away_team,
          placeholder_1: null,
          placeholder_2: null,
          stadium_id: match.stadium,
          score: null,
          winner: null
        }
    }));
});

let rawKnockoutMatches = [];

Object.keys(data.knockout).forEach(stage => {
    let stage_id = stageMapping['knockout'][stage];
    rawKnockoutMatches.push(...data.knockout[stage].matches.map(match => {
        match.stage_id = stage_id;
        return match;
    }));
});

function parseQualified(team) {
    let parts = team.split('_');

    if(parts[0] === "winner") {
        return `Vainqueur du groupe ${parts[1].toUpperCase()}`;
    } else if(parts[0] === "runner") {
        return `Second du groupe ${parts[1].toUpperCase()}`;
    }
}

function getFormattedPreviousStageName(currentStageId) {
    let previousStageKey = Object.keys(stageMapping['knockout']).find(stage => {
        return stageMapping['knockout'][stage] === currentStageId - 1
    });

    if(previousStageKey !== undefined) {
        let previousStageId = stageMapping['knockout'][previousStageKey];
        let previousStage = knockoutStages.find(stage => {
            return stage.id === previousStageId;
        });

        if(previousStage !== undefined) {
            switch(previousStage.name) {
                case 'Huitièmes de finale': return 'du huitième de finale';
                case 'Quarts de finale': return 'du quart de finale';
                case 'Demi-finales': return 'de la demi-finale';
            }
        }
    }


    throw "no valid previous stage";
}

function getPlaceholdersForMatch(match) {
    if(match.type === "qualified") {
        return [
            parseQualified(match.home_team),
            parseQualified(match.away_team)
        ];
    } else if (match.type === "winner") {
        let previousStageName = getFormattedPreviousStageName(match.stage_id);

        return [
            `Vainqueur ${previousStageName} ${match.home_team}`,
            `Vainqueur ${previousStageName} ${match.away_team}`
        ];
    } else if(match.type === "loser") {
        let previousStageName = getFormattedPreviousStageName(match.stage_id - 1);

        return [
            `Perdant ${previousStageName} ${match.home_team}`,
            `Perdant ${previousStageName} ${match.away_team}`
        ];
    }
}

knockoutMatches.push(...rawKnockoutMatches.map(match => {
    let placeholders = getPlaceholdersForMatch(match);

    return {
      id: match.name,
      stage_id: match.stage_id,
      match_time: getTimestampFromISODatetime(match.date),
      team_1_id: null,
      team_2_id: null,
      placeholder_1: placeholders[0],
      placeholder_2: placeholders[1],
      stadium_id: match.stadium,
      score: null,
      winner: null
    }
}));

matches.push(...groupMatches);
matches.push(...knockoutMatches);

matchStatements.push(...matches.map(match => {
    return `INSERT INTO matches(id, stages_id, match_time, team_1, team_2,
        placeholder_1, placeholder_2, stadiums_id, score, winner) VALUES (
        ${match.id},
        ${match.stage_id},
        ${toNULL(match.match_time, false, true)},
        ${toNULL(match.team_1_id)},
        ${toNULL(match.team_2_id)},
        ${toNULL(match.placeholder_1, true)},
        ${toNULL(match.placeholder_2, true)},
        ${toNULL(match.stadium_id)},
        ${toNULL(match.score, true)},
        ${toNULL(match.winner)});`.replace(/\n/g, '');
}));

let sqlStatements = [];
sqlStatements.push('DELETE FROM matches;');
sqlStatements.push('DELETE FROM stages;');
sqlStatements.push('DELETE FROM teams;');
sqlStatements.push('DELETE FROM stadiums;');
sqlStatements.push(...stadiumStatements);
sqlStatements.push(...stageStatements);
sqlStatements.push(...teamStatements);
sqlStatements.push(...matchStatements);

fs.writeFileSync('data.sql', sqlStatements.join('\n'));
