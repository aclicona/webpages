type PasswordErrorCode =
  | 'password_too_short'
  | 'password_too_common'
  | 'password_entirely_numeric'
  | 'password_too_similar'
  | 'password_no_letter'
  | 'password_no_number'
  | 'password_no_special'
  | 'passwords_do_not_match'
  | 'password_mismatch'
  | 'invalid_password'

type NonFieldErrors =
  | 'unauthenticated'
  | 'not_verified'
  | 'invalid_token'

// Single error object structure
export interface ValidationError {
  code: PasswordErrorCode | NonFieldErrors
  message?: string;
}


// Complete registration errors interface
export interface PasswordChangeErrors {
  // Field-specific errors
  newPassword2?: ValidationError[];
  nonFieldErrors?: ValidationError[];
  oldPassword?: ValidationError[];
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
export interface PasswordChangeErrorResponse {
  success: false;
  errors: PasswordChangeErrors;
}

// Helper type for successful registration
export interface PasswordChangeSuccessResponse {
  success: true;
  data: {
    userId: string;
    email: string;
    requiresEmailVerification: boolean;
  };
}

// Combined type for registration response
type RegistrationResponse = PasswordChangeErrorResponse | PasswordChangeSuccessResponse;

// Error message mapping
const ERROR_MESSAGES: Record<PasswordErrorCode | NonFieldErrors, string> = {
  password_too_short: 'La contraseña debe tener al menos 8 caracteres',
  password_too_common: 'La contraseña es demasiado común',
  password_entirely_numeric: 'La contraseña debe contener letras y números',
  password_too_similar: 'La contraseña es muy similar a tu información personal',
  password_no_letter: 'La contraseña debe contener al menos una letra',
  password_no_number: 'La contraseña debe contener al menos un número',
  password_no_special: 'La contraseña debe contener al menos un carácter especial',
  passwords_do_not_match: 'Las contraseñas no coinciden',
  unauthenticated: 'El usuario no está registrado y no puede realizar esta acción',
  not_verified: 'La cuenta no está verificada y no puede realizar esta acción',
  password_mismatch: 'Las contraseñas no coinciden',
  invalid_token: 'El token no es válido',
  invalid_password: 'La contraseña actual no es válida. Digita nuevamente tu contraseña'
}
export { ERROR_MESSAGES }