export default function useValidateEmail() {
  /**
   * Validates an email address using a comprehensive regular expression
   * This regex checks for:
   * - Proper email format (user@domain.tld)
   * - Allows for subdomain
   * - Allows for special characters in local part
   * - Prevents double dots
   * - Enforces valid TLD length
   *
   * @param email - The email address to validate
   * @returns boolean - True if email is valid, false otherwise
   */
  const isValidEmail = (email: string): boolean => {
    // Basic check for empty or whitespace
    if (!email || email.trim() === '') {
      return false
    }

    // Check maximum length (RFC 5321)
    if (email.length > 254) {
      return false
    }

    // Regular expression for email validation
    const emailRegex = /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/

    // Test the email against regex
    if (!emailRegex.test(email)) {
      return false
    }

    // Additional checks for common issues
    return !(email.includes('..') || // No consecutive dots
      email.startsWith('.') || // Don't start with dot
      email.endsWith('.') || // Don't end with dot
      !email.includes('@') || // Must contain @
      email.indexOf('@') !== email.lastIndexOf('@'))
  }
  return {
    isValidEmail
  }
}