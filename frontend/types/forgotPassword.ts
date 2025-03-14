type EmailErrors =
  | 'invalid'

type NonFieldErrors =
  | 'not_verified'
  | 'email_fail'

// Single error object structure
export interface ValidationError {
  code: EmailErrors | NonFieldErrors
  message?: string;
}

// Field-specific error arrays
interface FieldErrors {
  email?: ValidationError[];
  nonFieldErrors?: ValidationError[];
}

// Complete registration errors interface
export interface ForgotPasswordErrors {
  // Field-specific errors
  fieldErrors?: FieldErrors;

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

// Error message mapping
const ERROR_MESSAGES: Record<NonFieldErrors | EmailErrors, string> = {
  invalid: 'El correo electrónico no es válido',
  email_fail: 'Hubo un error enviando el correo, por favor intente de nuevo',
  not_verified: 'La cuenta no está verificada y no puede realizar esta acción'
}
export { ERROR_MESSAGES }