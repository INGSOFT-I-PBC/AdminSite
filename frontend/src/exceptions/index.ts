export class UserNotLoggedInError extends Error {
    constructor(message: Maybe<string> = "The current user isn't logged in") {
        super(message)
    }
}

export class SessionExpiredException extends Error {
    constructor() {
        super('The current session has been expired')
    }
}

export class UndersiredStateError extends Error {
    constructor(
        message: Maybe<string> = 'The current state of execution is not allowed'
    ) {
        super(message)
    }
}
