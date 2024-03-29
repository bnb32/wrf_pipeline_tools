
module get_date_mod

  use netcdf_driver_mod, only: ncfile_type, time_axis_index, &
                               get_axis_units, get_calendar_type

  use  time_manager_mod, only: time_type, set_date, get_date,   &
                               set_time, set_calendar_type,     &
                               operator(+), JULIAN, NO_LEAP,    &
                               THIRTY_DAY_MONTHS

  use     utilities_mod, only: error_mesg

  implicit none
  private


  public :: current_date
!!public :: get_ref_date, increment_date, to_time_type

contains

!#######################################################################

 subroutine get_ref_date (units, date)

  character(len=*), intent(in)  :: units
  integer         , intent(out) :: date(6)

  integer :: is, ie

!---- returns the reference date from time units label ----
!---- note: this version requires a specific format ----

  date = 0

  is = index(units, 'since')

  if ( is > 0 ) then
       ie = is + 24
       read (units(is:ie),10) date(1:6)
 10    format (6x,i4,5(1x,i2))      
  endif

 end subroutine get_ref_date

!#######################################################################

 subroutine increment_date (units, dt, date1, date2)

  character(len=*), intent(in)  :: units
  real,             intent(in)  :: dt
  integer,          intent(in)  :: date1(6)
  integer,          intent(out) :: date2(6)

  type(time_type) :: Time

!---- increments date1 by dt using time units label -----

  Time = set_date (date1(1), date1(2), date1(3), &
                   date1(4), date1(5), date1(6)) &
         + to_time_type (units,dt)

  call get_date (Time, date2(1), date2(2), date2(3), &
                       date2(4), date2(5), date2(6)  )

  date2(4) = get_hour(units,dt)

 end subroutine increment_date

!#######################################################################

 function to_time_type (units, time_since) result (Time)

   character(len=*), intent(in) :: units
   real            , intent(in) :: time_since
   type(time_type)              :: Time

   integer :: nc
   real    :: dfac 

!---- convert time_since to time_type ----
!---- valid time units are: seconds,minutes,hours,days ----- 

      nc = len_trim(units)

      if (index(units(1:nc),'sec') > 0) then
           dfac = 86400.
      else if (index(units(1:nc),'min') > 0) then
           dfac = 1440.
      else if (index(units(1:nc),'hour') > 0) then
           dfac = 24.
      else if (index(units(1:nc),'day') > 0) then
           dfac = 1.
      else
           call error_mesg ('to_time_type', 'invalid time units', 2)
           dfac = 1.
      endif

          Time = set_time (0,int(time_since/dfac))

 end function to_time_type

!#######################################################################
!#######################################################################

 function get_hour (units, time_since) result (hour)

   character(len=*), intent(in) :: units
   real            , intent(in) :: time_since
   integer :: nc
   real    :: rday, dfac
   integer :: hour

!---- convert time_since to time_type ----
!---- valid time units are: seconds,minutes,hours,days ----- 

      nc = len_trim(units)

      if (index(units(1:nc),'sec') > 0) then
           dfac = 86400.
      else if (index(units(1:nc),'min') > 0) then
           dfac = 1440.
      else if (index(units(1:nc),'hour') > 0) then
           dfac = 24.
      else if (index(units(1:nc),'day') > 0) then
           dfac = 1.
      else
           call error_mesg ('to_time_type', 'invalid time units', 2)
           dfac = 1.
      endif

            rday = time_since/dfac
            hour = nint( 24.0*(rday - int(rday)) )

 end function get_hour


!#######################################################################
!#######################################################################

 subroutine current_date (File, time_since, date)

  type(ncfile_type), intent(in)  :: File
  real,              intent(in)  :: time_since
  integer,           intent(out) :: date(6)

!  File       = ncfile_type from previous call to
!               read_file_header or write_file_header
!  time_since = time axis value
!  date       = date, dimension(6)=(year,month,day,hour,minute,seconds)

  integer :: axis, idate(6)
  logical :: uflag, cflag
  character(len=128) :: units, calendar

    date = 0
    axis = time_axis_index (File)

    uflag = get_axis_units    (File, axis, units)
    cflag = get_calendar_type (File, axis, calendar)

!---- no units, so return ----
    if (.not.uflag) return

!---- set calendar (default Julian ?) ----
    if (cflag) then
        call set_cal (calendar)
    else
        call set_cal ('NOLEAP')
    endif

!---- get reference date and increment using time_since ----

    call get_ref_date (units, idate)

    call increment_date (units, time_since, idate, date)

 end subroutine current_date
 
!#######################################################################

 subroutine set_cal (cal)

   character(len=*), intent(in) :: cal

    if (cal(1:6) == 'Julian'    .or.  &
        cal(1:6) == 'julian'    .or.  &
        cal(1:6) == 'JULIAN'    .or.  &
        cal(1:9) == 'Gregorian' .or.  &
        cal(1:9) == 'gregorian' .or.  &
        cal(1:9) == 'GREGORIAN' ) then
               call set_calendar_type (JULIAN)

!    else if (cal(1:6) == 'common') then
     else if (cal(1:6) == 'NOLEAP') then
               call set_calendar_type (NO_LEAP)

     else
!              call set_calendar_type (THIRTY_DAY_MONTHS)
               call set_calendar_type (NO_LEAP)
     endif

 end subroutine set_cal

!#######################################################################

end module get_date_mod

