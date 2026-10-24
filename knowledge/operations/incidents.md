
## Incident evt_1792457294_872 (2026-10-20)
- **Service**: dokter-v (`ihkaru/sipedas`)
- **Severity**: CRITICAL
- **Component**: `App\Filament\Resources\PenugasanResource\Widgets\PenugasanDisetujuiTable` (`export_excel`)
- **Error**: `FatalError: Maximum execution time of 30 seconds exceeded (/vendor/laravel/framework/src/Illuminate/Collections/Traits/EnumeratesValues.php:1145)`
- **Root Cause**:
  1. `TujuanSuratTugas::combinerTujuan` performed unindexed linear search `$masterSls->where(...)->first()` inside an iteration across 5,144 approved penugasan rows.
  2. `PenugasanDisetujuiExport` lacked eager loading of nested `tujuanSuratTugas` relations.
  3. `ShouldAutoSize` in Laravel Excel forced PhpSpreadsheet to iterate through font bounding boxes for 87,000+ cells.
  4. Missing time limit extension on large dataset export action.
- **Remediation**:
  1. Indexed `TujuanSuratTugas::combinerTujuan` with `keyBy` and relation checks.
  2. Added eager loading for `tujuanSuratTugas.desa`, `kecamatan`, `kabkot`, `provinsi`.
  3. Replaced `ShouldAutoSize` with `WithColumnWidths`.
  4. Added `@ini_set('max_execution_time', '300')` and `@set_time_limit(300)`.
- **Pull Request**: [#18](https://github.com/ihkaru/sipedas/pull/18) (`hotfix/auto-heal-3991264ca2ab48978a4aaa7673ffa8d5`)
- **Verification**: `php artisan test --filter PenugasanDisetujuiTableOptimizationTest` (7 passed, 34 assertions)

## Incident evt_1792459115_559 (2026-10-20)
- **Service**: dokter-v (`ihkaru/sipedas`)
- **Severity**: CRITICAL
- **Component**: `App\Filament\Resources\PenugasanResource\Widgets\PenugasanDisetujuiTable` (`export_excel`)
- **Error**: `FatalError: Maximum execution time of 30 seconds exceeded (/vendor/laravel/framework/src/Illuminate/Database/Eloquent/Concerns/HasTimestamps.php:179)`
- **Context**: Re-occurrence of 30s timeout on export_excel while PR #18 was pending merge.
- **Root Cause**: Identical to `evt_1792457294_872`. The script exceeded 30s during query execution / model instantiation while resolving timestamp columns (`getQualifiedCreatedAtColumn` at `HasTimestamps.php:179`).
- **Remediation**:
  1. Submitted PR [#19](https://github.com/ihkaru/sipedas/pull/19) on branch `hotfix/auto-heal-76fc868acbae4815913689c10968e448`.
  2. Applied hotfix directly to live production container `app-v7g6cdbkgsh4aa3xrqsb6u3g-20261019T042924` and reloaded FrankenPHP Octane workers.
  3. Live benchmark confirmed: Export time reduced from >30s (timeout) to **4.67s** (100% success).
- **Verification**: `php artisan test --filter PenugasanDisetujuiTableOptimizationTest` (7 passed, 34 assertions)

## Incident evt_1792552935_982 (2026-10-21)
- **Service**: dokter-v (`ihkaru/sipedas`)
- **Severity**: CRITICAL
- **Component**: Livewire Update Handler (`POST /livewire-2de9b0f2/update`)
- **Error**: `Livewire\Exceptions\PayloadTooLargeException: Livewire request payload is too large (1277KB). Maximum allowed size is 1024KB. You can configure this limit in config/livewire.php under 'payload.max_size'. (/public/frankenphp-worker.php:7)`
- **Root Cause**:
  1. Requests containing bulk records, large tables, or complex form states serialized by Livewire reached 1277KB.
  2. Livewire 3 validates request payload size against `config('livewire.payload.max_size')`.
  3. `config/livewire.php` lacked an explicit `payload` configuration block, falling back to Livewire's default 1024KB (1MB) limit.
- **Remediation**:
  1. Added `payload` configuration block in `config/livewire.php` setting `max_size` to `(int) env('LIVEWIRE_PAYLOAD_MAX_SIZE', 10 * 1024 * 1024)` (10MB), while retaining sensible protection against DoS (`max_nesting_depth: 10`, `max_calls: 50`, `max_components: 200`).
  2. Created `tests/bootstrap.php` and configured `phpunit.xml` to ensure clean PSR-4 resolution for unit test execution.
  3. Added `tests/Unit/LivewirePayloadConfigurationTest.php` verifying configuration values, safety limits, alert payload tolerance, and environment bindings.
  4. Submitted PR [#20](https://github.com/ihkaru/sipedas/pull/20) on branch `hotfix/auto-heal-3e7f8812a7614b14abf0dd3f56cbce83`.
  5. Hot-patched live production container `app-v7g6cdbkgsh4aa3xrqsb6u3g-20261019T042924`, cleared caches, and reloaded FrankenPHP Octane workers.
- **Verification**: `php artisan test tests/Unit/LivewirePayloadConfigurationTest.php` (4 passed, 12 assertions); live container confirmed `config('livewire.payload.max_size') = 10485760`.
