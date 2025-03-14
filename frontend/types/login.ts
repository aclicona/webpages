type CredentialsErrorCode =
  | 'invalid_credentials'

// Single error object structure
export interface ValidationError {
  code: CredentialsErrorCode;
  message?: string;
}

// Field-specific error arrays
export interface LoginErrors {
  nonFieldErrors?: ValidationError[];
  // General errors that aren't field-specific
  generalErrors?: string[];

  // Server or network related errors
  serverError?: {
    code: string;
    message: string;
  };

  // HTTP status code if applicable
  status?: number;

  // Flag to indicate if the error is from the client-side validation
  isClientValidation?: boolean;
}

// Helper type for registration error responses
export interface LoginErrorResponse {
  success: false;
  errors: LoginErrors;
}

// Helper type for successful registration
export interface LoginSuccessResponse {
  success: true;
  errors: []
  token: {
    token: string;
  }
  refreshToken: {
    token: string
  }
}

// Combined type for registration response
type LoginResponse = LoginErrorResponse | LoginSuccessResponse;

// Error message mapping
const ERROR_MESSAGES: Record<CredentialsErrorCode , string> = {
  invalid_credentials: 'El email y/o la constraseña son incorrectos',
}
export { ERROR_MESSAGES }