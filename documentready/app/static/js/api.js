/**
 * api.js — Fetch wrapper with error handling, timeout, and AbortController support.
 */

const DEFAULT_TIMEOUT_MS = 10000;
const API_BASE = '/api';

/**
 * Perform a fetch with timeout and standard error handling.
 * @param {string} path - URL path (relative to API_BASE or absolute)
 * @param {RequestInit} options - fetch options
 * @param {number} timeoutMs - timeout in milliseconds
 * @returns {Promise<any>} Parsed JSON data field
 */
export async function apiFetch(path, options = {}, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  const url = path.startsWith('http') ? path : `${API_BASE}${path}`;

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        ...(options.method === 'POST' ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    });

    clearTimeout(timeoutId);

    const json = await response.json();

    if (!response.ok) {
      const err = json?.error;
      throw new ApiError(
        err?.message || `HTTP ${response.status}`,
        err?.code || 'HTTP_ERROR',
        response.status,
        err?.details
      );
    }

    return json.data;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new ApiError('Request timed out', 'TIMEOUT', 0);
    }
    throw err;
  }
}

/**
 * GET wrapper.
 */
export function apiGet(path, params = {}, signal = null) {
  const url = new URL(path.startsWith('http') ? path : `${location.origin}${API_BASE}${path}`);
  for (const [k, v] of Object.entries(params)) {
    if (v !== null && v !== undefined && v !== '') url.searchParams.set(k, v);
  }
  // Remove origin to pass relative path to apiFetch, or just pass full url string
  return apiFetch(url.toString(), { signal });
}

/**
 * POST wrapper.
 */
export function apiPost(path, body = {}) {
  return apiFetch(path, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

/**
 * Custom error class for API errors.
 */
export class ApiError extends Error {
  constructor(message, code = 'UNKNOWN', status = 0, details = null) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
    this.details = details;
  }
}
