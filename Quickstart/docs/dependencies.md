# NPM DEPENDENCIES REQUIRED

    '''bash
    npm install --save-dev @commitlint/{config-conventional,cli} husky
    npx husky install
    '''
  ---

## commitlintrc.json

    '''json
    {
    "extends": ["@commitlint/config-conventional"]
    }

### Enable the Husky Hook

    '''bash

    npx husky add .husky/commit-msg "npx --no -- commitlint --edit $1"
    git add .husky/commit-msg

    '''
